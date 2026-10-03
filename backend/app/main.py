from fastapi import FastAPI, Depends

from app.dependencies import get_current_user
from app.database import engine, Base
from app import models
from app.users import router as users_router
from app.datasets import router as datasets_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="InsightAI API",
    description="AI-Powered Data Analytics SaaS Platform",
    version="1.0.0"
)

app.include_router(users_router)
app.include_router(datasets_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to InsightAI API",
        "status": "running"
    }

@app.get("/protected")
def protected_route(
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "You accessed a protected API",
        "user": current_user
    }