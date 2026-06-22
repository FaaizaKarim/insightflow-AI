"""
Text-to-SQL tool with safety guardrails.
- Schema-aware: injects column names to prevent hallucination
- SELECT only: blocks any mutating statements
- Table whitelist: only allowed tables can be queried
"""
import re
from langchain_core.tools import tool
from sqlalchemy import text, create_engine, inspect
from app.core.config import settings

ALLOWED_TABLES = {"customers", "orders", "interactions"}
FORBIDDEN_KEYWORDS = {"insert", "update", "delete", "drop", "alter", "create", "truncate", "exec", "execute"}

# Sync engine for tool use (tools are called synchronously by LangGraph)
_sync_engine = None


def get_sync_engine():
    global _sync_engine
    if _sync_engine is None:
        _sync_engine = create_engine(settings.DATABASE_SYNC_URL)
    return _sync_engine


def get_schema_context() -> str:
    """Return table schemas as context for the LLM."""
    try:
        engine = get_sync_engine()
        inspector = inspect(engine)
        lines = []
        for table in ALLOWED_TABLES:
            try:
                cols = inspector.get_columns(table)
                col_desc = ", ".join(f"{c['name']} ({str(c['type'])})" for c in cols)
                lines.append(f"Table `{table}`: {col_desc}")
            except Exception:
                pass
        return "\n".join(lines)
    except Exception as e:
        return f"Schema unavailable: {e}"


def validate_sql(sql: str) -> tuple[bool, str]:
    """Validate SQL is safe to execute."""
    sql_lower = sql.lower().strip()

    # Must be SELECT
    if not sql_lower.startswith("select"):
        return False, "Only SELECT statements are allowed."

    # Check for forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_lower):
            return False, f"Keyword '{keyword}' is not permitted."

    # Check for allowed tables only
    mentioned_tables = re.findall(r"from\s+(\w+)|join\s+(\w+)", sql_lower)
    for match in mentioned_tables:
        table = (match[0] or match[1]).lower()
        if table and table not in ALLOWED_TABLES:
            return False, f"Table '{table}' is not in the allowed list: {ALLOWED_TABLES}"

    return True, "OK"


@tool
def sql_query_tool(natural_language_question: str) -> str:
    """
    Convert a natural language business question into SQL and execute it against the database.
    Returns results as a formatted table. Use for questions about customers, orders, revenue, regions.
    
    Args:
        natural_language_question: The business question in plain English.
    """
    from langchain_anthropic import ChatAnthropic
    from app.core.config import settings

    schema = get_schema_context()

    prompt = f"""You are a SQL expert. Convert the following business question to a PostgreSQL SELECT query.

Database schema:
{schema}

Rules:
- Only use tables: customers, orders, interactions
- Only write SELECT statements
- Limit results to 50 rows unless asked for more
- Use proper JOINs when needed
- Return ONLY the SQL query, nothing else

Question: {natural_language_question}

SQL:"""

    try:
        llm = ChatAnthropic(
            model=settings.LLM_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0,
        )
        response = llm.invoke(prompt)
        sql = response.content.strip().strip("```sql").strip("```").strip()

        # Validate
        valid, reason = validate_sql(sql)
        if not valid:
            return f"SQL validation failed: {reason}. Generated SQL: {sql}"

        # Execute
        engine = get_sync_engine()
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()
            columns = list(result.keys())

        if not rows:
            return "Query returned no results."

        # Format as markdown table
        header = "| " + " | ".join(columns) + " |"
        divider = "| " + " | ".join(["---"] * len(columns)) + " |"
        data_rows = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows[:50]]

        return f"**SQL Query:** `{sql}`\n\n**Results ({len(rows)} rows):**\n\n{header}\n{divider}\n" + "\n".join(data_rows)

    except Exception as e:
        return f"Database error: {str(e)}"
