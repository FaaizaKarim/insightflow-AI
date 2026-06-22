from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from app.core.config import settings
from app.db.database import engine, Base
from app.api.routes import chat, predict, query, ingest
from app.ml.predict import load_model
from app.agents.graph import build_agent

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    logger.info("InsightFlow AI starting up...")

    # Create DB tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Load ML model into app state
    app.state.ml_model, app.state.ml_scaler = load_model()

    # Build LangGraph agent
    app.state.agent = build_agent()

    logger.info("Startup complete. All systems ready.")
    yield

    logger.info("Shutting down...")
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Data Intelligence Agent — SQL · ML · RAG",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(predict.router, prefix="/api/v1/predict", tags=["ML Predict"])
app.include_router(query.router, prefix="/api/v1/query", tags=["SQL Query"])
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["Document Ingest"])


@app.get("/health")
async def health():
    return {"status": "ok", "version": settings.APP_VERSION}
