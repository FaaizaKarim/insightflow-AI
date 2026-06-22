"""
Tests for ML prediction logic.
"""
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from app.ml.predict import predict_single


def make_mock_model(churn_prob=0.75):
    model = MagicMock()
    model.predict_proba.return_value = np.array([[1 - churn_prob, churn_prob]])
    return model


def make_mock_scaler():
    scaler = MagicMock()
    scaler.transform.side_effect = lambda x: x
    return scaler


def test_high_churn_prediction():
    model = make_mock_model(churn_prob=0.85)
    scaler = make_mock_scaler()
    features = {
        "total_orders": 1, "avg_order_value": 100,
        "days_since_last_order": 120, "total_interactions": 5,
        "avg_sentiment": -0.5, "unresolved_interactions": 3,
        "contract_value": 500, "account_age_days": 90,
    }
    result = predict_single(model, scaler, features)
    assert result["prediction"] == "churn"
    assert result["churn_probability"] > 0.5


def test_low_churn_prediction():
    model = make_mock_model(churn_prob=0.1)
    scaler = make_mock_scaler()
    features = {
        "total_orders": 10, "avg_order_value": 2000,
        "days_since_last_order": 5, "total_interactions": 2,
        "avg_sentiment": 0.8, "unresolved_interactions": 0,
        "contract_value": 10000, "account_age_days": 500,
    }
    result = predict_single(model, scaler, features)
    assert result["prediction"] == "retain"
    assert result["churn_probability"] < 0.5


def test_probabilities_sum_to_one():
    model = make_mock_model(churn_prob=0.42)
    scaler = make_mock_scaler()
    result = predict_single(model, scaler, {})
    assert abs(result["churn_probability"] + result["no_churn_probability"] - 1.0) < 1e-6
