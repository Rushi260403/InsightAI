from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "message": "You are authenticated!",
        "user": current_user["user_id"]
    }