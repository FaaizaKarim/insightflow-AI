"""
ML Prediction Tool — wraps scikit-learn churn model as a LangGraph tool.
"""
import json
import numpy as np
from langchain_core.tools import tool
from app.core.config import settings


def _get_model():
    """Lazy-load the ML model from disk."""
    import joblib
    try:
        model = joblib.load(settings.MODEL_PATH)
        scaler = joblib.load(settings.SCALER_PATH)
        return model, scaler
    except FileNotFoundError:
        return None, None


# Feature columns expected by the model
FEATURE_COLUMNS = [
    "total_orders",
    "avg_order_value",
    "days_since_last_order",
    "total_interactions",
    "avg_sentiment",
    "unresolved_interactions",
    "contract_value",
    "account_age_days",
]


@tool
def ml_predict_tool(customer_data: str) -> str:
    """
    Run churn prediction on one or more customers using the trained scikit-learn model.
    
    Args:
        customer_data: JSON string with customer features. Can be a single dict or list of dicts.
                       Required fields: total_orders, avg_order_value, days_since_last_order,
                       total_interactions, avg_sentiment, unresolved_interactions,
                       contract_value, account_age_days.
                       Optionally include 'customer_id' and 'name' for labeling.
    
    Returns:
        Churn predictions with probability scores.
    """
    try:
        data = json.loads(customer_data)
        if isinstance(data, dict):
            data = [data]

        model, scaler = _get_model()
        if model is None:
            return "ML model not loaded. Run `python scripts/train_model.py` first."

        results = []
        for customer in data:
            features = np.array([[customer.get(col, 0) for col in FEATURE_COLUMNS]])
            features_scaled = scaler.transform(features)
            prob = model.predict_proba(features_scaled)[0]
            churn_prob = float(prob[1])
            prediction = "HIGH RISK" if churn_prob > 0.7 else "MEDIUM RISK" if churn_prob > 0.4 else "LOW RISK"

            result = {
                "customer_id": customer.get("customer_id", "N/A"),
                "name": customer.get("name", "Unknown"),
                "churn_probability": round(churn_prob * 100, 1),
                "risk_level": prediction,
                "top_risk_factors": _explain_risk(customer, churn_prob),
            }
            results.append(result)

        # Format output
        lines = ["**Churn Prediction Results:**\n"]
        for r in results:
            lines.append(
                f"- **{r['name']}** (ID: {r['customer_id']}): "
                f"{r['risk_level']} — {r['churn_probability']}% churn probability\n"
                f"  Risk factors: {', '.join(r['top_risk_factors'])}"
            )
        return "\n".join(lines)

    except json.JSONDecodeError:
        return "Invalid JSON input. Please provide customer data as a valid JSON string."
    except Exception as e:
        return f"Prediction error: {str(e)}"


def _explain_risk(customer: dict, churn_prob: float) -> list[str]:
    """Simple rule-based risk factor explanation."""
    factors = []
    if customer.get("days_since_last_order", 0) > 60:
        factors.append("no recent orders (60+ days)")
    if customer.get("avg_sentiment", 0) < -0.2:
        factors.append("negative support sentiment")
    if customer.get("unresolved_interactions", 0) > 2:
        factors.append("unresolved support tickets")
    if customer.get("total_orders", 0) < 3:
        factors.append("low order history")
    if not factors:
        factors.append("model pattern — review account manually")
    return factors
