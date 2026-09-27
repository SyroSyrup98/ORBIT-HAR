from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from datetime import datetime

import cv2
import threading
import time

from .camera import camera
from .detector import ObjectDetector
from .pose import PoseEstimator
from .features import extract_features
from .interaction import analyze_hand_object_interaction
from .temporal import TemporalBuffer
from .object_tracker import ObjectTracker
from .recording_controller import RecordingController
from .recorder import ActionRecorder


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="ORBIT-HAR Backend",
    description="Onboard experiment assistant backend",
    version="0.1.0",
)


# ============================================================
# AI COMPONENTS
# ============================================================

detector = ObjectDetector()

pose_estimator = PoseEstimator()

temporal_buffer = TemporalBuffer(
    max_length=30
)

object_tracker = ObjectTracker()


# ============================================================
# DATA RECORDING
# ============================================================

recording_controller = RecordingController(
    sequence_length=30
)

action_recorder = ActionRecorder()


# ============================================================
# SHARED PERCEPTION STATE
# ============================================================

latest_detections = []

latest_pose = None

latest_features = None

state_lock = threading.Lock()


# ============================================================
# PERCEPTION THREAD
# ============================================================

perception_thread = None

perception_running = False


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup():

    global perception_thread
    global perception_running

    camera.start()

    perception_running = True

    perception_thread = threading.Thread(
        target=perception_loop,
        daemon=True,
    )

    perception_thread.start()

    print(
        "ORBIT-HAR perception system started."
    )


# ============================================================
# SHUTDOWN
# ============================================================

@app.on_event("shutdown")
def shutdown():

    global perception_running

    perception_running = False

    camera.stop()

    pose_estimator.close()

    print(
        "ORBIT-HAR perception system stopped."
    )


# ============================================================
# PERCEPTION LOOP
# ============================================================

def perception_loop():

    global latest_detections
    global latest_pose
    global latest_features

    while perception_running:

        # ----------------------------------------------------
        # GET LATEST CAMERA FRAME
        # ----------------------------------------------------

        frame = camera.get_frame()

        if frame is None:

            time.sleep(0.01)

            continue


        # ====================================================
        # YOLO OBJECT DETECTION
        # ====================================================

        try:

            detections = detector.detect(
                frame
            )

            movement_features = (
                object_tracker.update(
                    detections=detections,
                    frame_width=frame.shape[1],
                    frame_height=frame.shape[0],
                )
            )

            with state_lock:

                latest_detections = detections

        except Exception as error:

            print(
                f"YOLO error: {error}"
            )

            detections = []

            movement_features = {
                "object_moving": False,
                "object_speed": 0.0,
                "tracked_object": None,
            }


        # ====================================================
        # POSE ESTIMATION
        # ====================================================

        try:

            pose_result = pose_estimator.detect(
                frame
            )

            pose_data = []


            # ------------------------------------------------
            # EXTRACT RAW LANDMARKS
            # ------------------------------------------------

            if pose_result.pose_landmarks:

                for landmark in pose_result.pose_landmarks[0]:

                    pose_data.append({
                        "x": landmark.x,
                        "y": landmark.y,
                        "z": landmark.z,
                        "visibility": landmark.visibility,
                    })


            # ------------------------------------------------
            # STORE RAW POSE
            # ------------------------------------------------

            with state_lock:

                latest_pose = pose_data


            # =================================================
            # POSE FEATURES
            # =================================================

            features = extract_features(
                pose_data
                if pose_data
                else None
            )


            # =================================================
            # HAND / OBJECT INTERACTION
            # =================================================

            interaction_features = (
                analyze_hand_object_interaction(

                    landmarks=pose_data,

                    detections=detections,

                    frame_width=frame.shape[1],

                    frame_height=frame.shape[0],
                )
            )


            # =================================================
            # COMBINE FEATURES
            # =================================================

            if features is not None:

                features.update(
                    interaction_features
                )

                features.update(
                    movement_features
                )


                # ------------------------------------------------
                # TEMPORAL BUFFER
                # ------------------------------------------------

                temporal_buffer.add(
                    features
                )


                # ------------------------------------------------
                # MANUAL ACTION RECORDING
                # ------------------------------------------------

                recording_complete = (
                    recording_controller.add_frame(
                        features
                    )
                )


                # ------------------------------------------------
                # SAVE COMPLETED SEQUENCE
                # ------------------------------------------------

                if recording_complete:

                    sequence = (
                        recording_controller
                        .get_sequence()
                    )

                    action = (
                        recording_controller.action
                    )

                    action_recorder.save_sequence(
                        action,
                        sequence
                    )

                    recording_controller.reset()

                    print(
                        f"Recording completed: {action}"
                    )


            # ------------------------------------------------
            # STORE LATEST FEATURES
            # ------------------------------------------------

            with state_lock:

                latest_features = features


        except Exception as error:

            print(
                f"Pose error: {error}"
            )


        # ----------------------------------------------------
        # SMALL CPU YIELD
        # ----------------------------------------------------

        time.sleep(0.01)


# ============================================================
# BASIC API
# ============================================================

@app.get("/")
def root():

    return {
        "system": "ORBIT-HAR",
        "status": "online",
        "message": "Backend is running",
    }


# ============================================================
# HEALTH API
# ============================================================

@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


# ============================================================
# PERCEPTION STATUS API
# ============================================================

@app.get("/api/status")
def status():

    with state_lock:

        detections = (
            latest_detections.copy()
        )

        pose = (
            latest_pose.copy()
            if latest_pose is not None
            else None
        )

        features = (
            latest_features.copy()
            if latest_features is not None
            else None
        )


    return {

        "system": "ORBIT-HAR",

        "state": "PERCEPTION_ACTIVE",

        "activity": None,

        "object": None,

        "confidence": None,

        "current_step": 0,

        "total_steps": 0,

        "detections": detections,

        "pose_landmarks": pose,

        "features": features,

        "temporal_buffer": {

            "size": len(
                temporal_buffer
            ),

            "ready": (
                temporal_buffer.is_ready()
            ),
        },

        "recording": (
            recording_controller.progress()
        ),
    }


# ============================================================
# START ACTION RECORDING
# ============================================================

@app.post("/api/record/start/{action}")
def start_recording(action: str):

    action = action.upper()

    allowed_actions = {
        "REACH",
        "PICK_UP",
        "MOVE",
        "PLACE",
    }

    if action not in allowed_actions:

        return {
            "success": False,
            "message": (
                f"Invalid action: {action}"
            ),
            "allowed_actions": sorted(
                allowed_actions
            ),
        }


    success = (
        recording_controller.start(
            action
        )
    )


    if not success:

        return {
            "success": False,
            "message": (
                "A recording is already active."
            ),
            "recording": (
                recording_controller.progress()
            ),
        }


    return {
        "success": True,
        "message": (
            f"Recording started: {action}"
        ),
        "recording": (
            recording_controller.progress()
        ),
    }


# ============================================================
# RESET RECORDING
# ============================================================

@app.post("/api/record/reset")
def reset_recording():

    recording_controller.reset()

    return {
        "success": True,
        "message": "Recording reset.",
        "recording": (
            recording_controller.progress()
        ),
    }


# ============================================================
# DRAW POSE
# ============================================================

def draw_pose(
    frame,
    pose,
):

    if not pose:

        return


    height, width = (
        frame.shape[:2]
    )


    for landmark in pose:

        x = int(
            landmark["x"] * width
        )

        y = int(
            landmark["y"] * height
        )


        if (
            x < 0
            or x >= width
            or y < 0
            or y >= height
        ):

            continue


        cv2.circle(

            frame,

            (x, y),

            4,

            (0, 255, 255),

            -1,
        )


# ============================================================
# LIVE VIDEO STREAM
# ============================================================

def generate_frames():

    while True:

        frame = camera.get_frame()

        if frame is None:

            time.sleep(0.01)

            continue


        # ----------------------------------------------------
        # GET LATEST AI STATE
        # ----------------------------------------------------

        with state_lock:

            detections = (
                latest_detections.copy()
            )

            pose = (
                latest_pose.copy()
                if latest_pose is not None
                else None
            )


        # ====================================================
        # DRAW YOLO DETECTIONS
        # ====================================================

        for detection in detections:

            x1, y1, x2, y2 = (
                detection["bbox"]
            )

            label = (
                detection["class_name"]
            )

            confidence = (
                detection["confidence"]
            )


            cv2.rectangle(

                frame,

                (x1, y1),

                (x2, y2),

                (0, 255, 0),

                2,
            )


            cv2.putText(

                frame,

                f"{label} {confidence:.2f}",

                (
                    x1,
                    max(
                        y1 - 10,
                        20
                    ),
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (0, 255, 0),

                2,
            )


        # ====================================================
        # DRAW POSE LANDMARKS
        # ====================================================

        draw_pose(
            frame,
            pose,
        )


        # ====================================================
        # ENCODE FRAME
        # ====================================================

        success, buffer = (
            cv2.imencode(
                ".jpg",
                frame,
            )
        )

        if not success:

            continue


        # ====================================================
        # MJPEG STREAM
        # ====================================================

        yield (

            b"--frame\r\n"

            b"Content-Type: image/jpeg\r\n\r\n"

            + buffer.tobytes()

            + b"\r\n"
        )


# ============================================================
# CAMERA ENDPOINT
# ============================================================

@app.get("/api/camera")
def camera_feed():

    return StreamingResponse(

        generate_frames(),

        media_type=(
            "multipart/x-mixed-replace;"
            " boundary=frame"
        ),
    )