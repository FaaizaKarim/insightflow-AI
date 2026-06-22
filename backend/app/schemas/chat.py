from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    message: str
    session_id: str
    history: Optional[List[dict]] = []


class ChatResponse(BaseModel):
    content: str
    session_id: str
    tool_calls: List[str] = []


class PredictRequest(BaseModel):
    customer_id: Optional[int] = None
    total_orders: float = 0
    avg_order_value: float = 0
    days_since_last_order: float = 0
    total_interactions: float = 0
    avg_sentiment: float = 0
    unresolved_interactions: float = 0
    contract_value: float = 0
    account_age_days: float = 0


class PredictResponse(BaseModel):
    customer_id: Optional[int]
    churn_probability: float
    no_churn_probability: float
    prediction: str
    risk_level: str
