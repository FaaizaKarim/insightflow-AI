from fastapi import APIRouter, Request, HTTPException
from app.schemas.chat import PredictRequest, PredictResponse
from app.ml.predict import predict_single

router = APIRouter()


@router.post("/", response_model=PredictResponse)
async def predict_churn(request: Request, body: PredictRequest):
    """Run churn prediction for a customer."""
    model = request.app.state.ml_model
    scaler = request.app.state.ml_scaler

    if model is None:
        raise HTTPException(status_code=503, detail="ML model not loaded. Run train_model.py first.")

    features = body.model_dump(exclude={"customer_id"})
    result = predict_single(model, scaler, features)

    risk_level = (
        "HIGH" if result["churn_probability"] > 0.7
        else "MEDIUM" if result["churn_probability"] > 0.4
        else "LOW"
    )

    return PredictResponse(
        customer_id=body.customer_id,
        churn_probability=round(result["churn_probability"], 4),
        no_churn_probability=round(result["no_churn_probability"], 4),
        prediction=result["prediction"],
        risk_level=risk_level,
    )
