"""
Churn prediction model training pipeline.
Trains on the PostgreSQL dataset seeded by seed_db.py.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_SYNC_URL", "postgresql://insightflow:insightflow@localhost:5432/insightflow")
MODEL_PATH = os.getenv("MODEL_PATH", "app/ml/models/churn_model.pkl")
SCALER_PATH = os.getenv("SCALER_PATH", "app/ml/models/scaler.pkl")


def build_features(engine) -> pd.DataFrame:
    """Build feature matrix from database."""
    query = """
    SELECT
        c.id AS customer_id,
        c.name,
        c.contract_value,
        c.is_churned,
        EXTRACT(DAY FROM NOW() - c.created_at) AS account_age_days,
        COALESCE(o.total_orders, 0) AS total_orders,
        COALESCE(o.avg_order_value, 0) AS avg_order_value,
        COALESCE(EXTRACT(DAY FROM NOW() - o.last_order_date), 999) AS days_since_last_order,
        COALESCE(i.total_interactions, 0) AS total_interactions,
        COALESCE(i.avg_sentiment, 0) AS avg_sentiment,
        COALESCE(i.unresolved_interactions, 0) AS unresolved_interactions
    FROM customers c
    LEFT JOIN (
        SELECT customer_id,
               COUNT(*) AS total_orders,
               AVG(amount) AS avg_order_value,
               MAX(created_at) AS last_order_date
        FROM orders
        GROUP BY customer_id
    ) o ON c.id = o.customer_id
    LEFT JOIN (
        SELECT customer_id,
               COUNT(*) AS total_interactions,
               AVG(sentiment) AS avg_sentiment,
               SUM(CASE WHEN resolved = false THEN 1 ELSE 0 END) AS unresolved_interactions
        FROM interactions
        GROUP BY customer_id
    ) i ON c.id = i.customer_id
    """
    return pd.read_sql(query, engine)


def train():
    engine = create_engine(DATABASE_URL)
    print("Building feature matrix...")
    df = build_features(engine)

    FEATURE_COLS = [
        "total_orders", "avg_order_value", "days_since_last_order",
        "total_interactions", "avg_sentiment", "unresolved_interactions",
        "contract_value", "account_age_days",
    ]

    X = df[FEATURE_COLS].fillna(0)
    y = df["is_churned"].astype(int)

    print(f"Dataset: {len(df)} customers, {y.sum()} churned ({y.mean()*100:.1f}%)")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        random_state=42,
    )
    print("Training model...")
    model.fit(X_train_s, y_train)

    y_pred = model.predict(X_test_s)
    y_prob = model.predict_proba(X_test_s)[:, 1]

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")

    # Feature importance
    print("\nFeature Importances:")
    for feat, imp in sorted(zip(FEATURE_COLS, model.feature_importances_), key=lambda x: -x[1]):
        print(f"  {feat}: {imp:.4f}")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"\nModel saved to {MODEL_PATH}")
    print(f"Scaler saved to {SCALER_PATH}")


if __name__ == "__main__":
    train()
