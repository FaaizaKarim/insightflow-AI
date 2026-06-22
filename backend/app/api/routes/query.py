from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.tools.sql_tool import sql_query_tool

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/")
async def run_query(body: QueryRequest):
    """Run a natural language query directly against the database (bypasses the agent)."""
    try:
        result = sql_query_tool.invoke({"natural_language_question": body.question})
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
