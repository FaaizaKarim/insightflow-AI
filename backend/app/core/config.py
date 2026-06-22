from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "InsightFlow AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # LLM
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "anthropic"  # "anthropic" or "openai"
    LLM_MODEL: str = "claude-3-5-sonnet-20241022"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://insightflow:insightflow@db:5432/insightflow"
    DATABASE_SYNC_URL: str = "postgresql://insightflow:insightflow@db:5432/insightflow"

    # ChromaDB
    CHROMA_HOST: str = "chroma"
    CHROMA_PORT: int = 8001
    CHROMA_COLLECTION: str = "company_docs"

    # Embedding model
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # ML
    MODEL_PATH: str = "/app/ml/models/churn_model.pkl"
    SCALER_PATH: str = "/app/ml/models/scaler.pkl"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
