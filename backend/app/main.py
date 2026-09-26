from fastapi import FastAPI
from datetime import datetime


app = FastAPI(
    title="ORBIT-HAR Backend",
    description="Onboard experiment assistant backend",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "system": "ORBIT-HAR",
        "status": "online",
        "message": "Backend is running",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/status")
def status():
    return {
        "system": "ORBIT-HAR",
        "state": "IDLE",
        "activity": None,
        "object": None,
        "confidence": None,
        "current_step": 0,
        "total_steps": 0,
    }