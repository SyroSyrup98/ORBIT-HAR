from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from datetime import datetime
import cv2

from .camera import camera


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
        "state": "CAMERA_READY",
        "activity": None,
        "object": None,
        "confidence": None,
        "current_step": 0,
        "total_steps": 0,
    }


def generate_frames():
    camera.start()

    while True:
        frame = camera.read()

        success, buffer = cv2.imencode(".jpg", frame)

        if not success:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


@app.get("/api/camera")
def camera_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )