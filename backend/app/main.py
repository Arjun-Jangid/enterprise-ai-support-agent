from fastapi import FastAPI
from backend.app.api.routes import router
from backend.app.api.chat_routes import router as chat_router
from backend.app.db.connection import engine, Base
from backend.app.core.logging_config import logger


app = FastAPI(title="My FastAPI Application", description="This is a sample FastAPI application.", version="1.0.0")

logger.info("Enterprise AI Support Agent backend started")

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")
app.include_router(chat_router, prefix="/api")