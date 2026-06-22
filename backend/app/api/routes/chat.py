from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage
import json
import asyncio

from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.graph import run_agent
from app.db.database import AsyncSessionLocal
from app.db import models

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest):
    """Send a message to the InsightFlow AI agent."""
    agent = request.app.state.agent

    # Reconstruct message history
    history = []
    for msg in body.history:
        if msg.get("role") == "user":
            history.append(HumanMessage(content=msg["content"]))
        elif msg.get("role") == "assistant":
            history.append(AIMessage(content=msg["content"]))

    try:
        result = await run_agent(agent, body.session_id, body.message, history)

        # Persist to DB
        async with AsyncSessionLocal() as db:
            session = models.ChatSession(session_id=body.session_id, user_id="default")
            db.add(session)
            await db.flush()

            db.add(models.ChatMessage(session_id=session.id, role="user", content=body.message))
            db.add(models.ChatMessage(
                session_id=session.id,
                role="assistant",
                content=result["content"],
                tool_calls=json.dumps(result["tool_calls"]),
            ))
            await db.commit()

        return ChatResponse(
            content=result["content"],
            session_id=body.session_id,
            tool_calls=result["tool_calls"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_history(session_id: str):
    """Retrieve chat history for a session."""
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        stmt = (
            select(models.ChatMessage)
            .join(models.ChatSession)
            .where(models.ChatSession.session_id == session_id)
            .order_by(models.ChatMessage.created_at)
        )
        result = await db.execute(stmt)
        messages = result.scalars().all()
        return [{"role": m.role, "content": m.content, "created_at": m.created_at} for m in messages]
