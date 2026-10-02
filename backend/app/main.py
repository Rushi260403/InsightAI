from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="InsightAI API",
    description="AI-Powered Data Analytics SaaS Platform",
    version="1.0.0"
)

app.include_router(users_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to InsightAI API",
        "status": "running"
    }