from fastapi import FastAPI

app = FastAPI(
    title="InsightAI API",
    description="AI-Powered Data Analytics SaaS Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to InsightAI API",
        "status": "running"
    }