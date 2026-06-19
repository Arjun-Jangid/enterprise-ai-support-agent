from fastapi import FastAPI
from backend.app.api.routes import router
from backend.app.db.connection import engine, Base


app = FastAPI(title="My FastAPI Application", description="This is a sample FastAPI application.", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(router)