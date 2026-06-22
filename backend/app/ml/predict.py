import joblib
import numpy as np
from app.core.config import settings


def load_model():
    """Load the trained model and scaler from disk."""
    try:
        model = joblib.load(settings.MODEL_PATH)
        scaler = joblib.load(settings.SCALER_PATH)
        return model, scaler
    except FileNotFoundError:
        return None, None


def predict_single(model, scaler, features: dict) -> dict:
    """Run inference for a single customer."""
    FEATURE_COLS = [
        "total_orders", "avg_order_value", "days_since_last_order",
        "total_interactions", "avg_sentiment", "unresolved_interactions",
        "contract_value", "account_age_days",
    ]
    X = np.array([[features.get(col, 0) for col in FEATURE_COLS]])
    X_scaled = scaler.transform(X)
    prob = model.predict_proba(X_scaled)[0]
    return {
        "churn_probability": float(prob[1]),
        "no_churn_probability": float(prob[0]),
        "prediction": "churn" if prob[1] > 0.5 else "retain",
    }
