from langchain_core.messages import AIMessage
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.tools.sql_tool import sql_query_tool
from app.tools.ml_tool import ml_predict_tool
from app.tools.rag_tool import rag_search_tool
from app.agents.prompts import SYSTEM_PROMPT


def get_llm():
    tools = [sql_query_tool, ml_predict_tool, rag_search_tool]
    if settings.LLM_PROVIDER == "anthropic":
        llm = ChatAnthropic(
            model=settings.LLM_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0,
        )
    else:
        llm = ChatOpenAI(
            model="gpt-4o",
            api_key=settings.OPENAI_API_KEY,
            temperature=0,
        )
    return llm.bind_tools(tools)


_llm = None


def call_model(state):
    """Agent node: call the LLM with current message history."""
    global _llm
    if _llm is None:
        _llm = get_llm()

    messages = state["messages"]

    # Prepend system prompt on first call
    from langchain_core.messages import SystemMessage
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

    response = _llm.invoke(messages)

    # Track which tools were called
    tool_calls_made = state.get("tool_calls_made", [])
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tc in response.tool_calls:
            tool_calls_made.append(tc["name"])

    return {
        "messages": [response],
        "tool_calls_made": tool_calls_made,
    }


def should_continue(state) -> str:
    """Decide whether to run tools or end the conversation turn."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"
