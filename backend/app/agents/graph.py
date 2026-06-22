"""
InsightFlow AI — LangGraph Agent
Routes user questions to SQL, ML prediction, or RAG tools.
"""
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from app.agents.nodes import call_model, should_continue
from app.tools.sql_tool import sql_query_tool
from app.tools.ml_tool import ml_predict_tool
from app.tools.rag_tool import rag_search_tool


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    session_id: str
    tool_calls_made: list[str]


def build_agent():
    """Build and compile the LangGraph agent."""
    tools = [sql_query_tool, ml_predict_tool, rag_search_tool]
    tool_node = ToolNode(tools)

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("agent", call_model)
    graph.add_node("tools", tool_node)

    # Edges
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )
    graph.add_edge("tools", "agent")

    return graph.compile()


async def run_agent(agent, session_id: str, user_message: str, history: list) -> dict:
    """Run the agent with a user message and return the response."""
    messages = history + [HumanMessage(content=user_message)]

    result = await agent.ainvoke({
        "messages": messages,
        "session_id": session_id,
        "tool_calls_made": [],
    })

    final_message = result["messages"][-1]
    tool_calls_made = result.get("tool_calls_made", [])

    return {
        "content": final_message.content,
        "tool_calls": tool_calls_made,
        "messages": result["messages"],
    }
