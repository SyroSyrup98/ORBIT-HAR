from pathlib import Path

import cv2
import mediapipe as mp


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "pose_landmarker_lite.task"


class PoseEstimator:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Pose model not found: {MODEL_PATH}"
            )

        base_options = mp.tasks.BaseOptions(
            model_asset_path=str(MODEL_PATH)
        )

        options = mp.tasks.vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.IMAGE,
            num_poses=1,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.landmarker = mp.tasks.vision.PoseLandmarker.create_from_options(
            options
        )

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb,
        )

        result = self.landmarker.detect(image)

        return result

    def close(self):
        self.landmarker.close()