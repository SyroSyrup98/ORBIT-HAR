import cv2
import threading


class Camera:
    def __init__(self, camera_index=1):
        self.camera_index = camera_index

        self.capture = None
        self.latest_frame = None

        self.running = False
        self.lock = threading.Lock()
        self.thread = None

    def start(self):
        if self.running:
            return

        self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            raise RuntimeError(
                f"Could not open camera {self.camera_index}"
            )

        # Keep camera capture reasonably lightweight.
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.running = True

        self.thread = threading.Thread(
            target=self._capture_loop,
            daemon=True,
        )

        self.thread.start()

    def _capture_loop(self):
        while self.running:
            success, frame = self.capture.read()

            if not success:
                continue

            with self.lock:
                self.latest_frame = frame

    def get_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None

            return self.latest_frame.copy()

    def stop(self):
        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=1)

        if self.capture is not None:
            self.capture.release()

        self.capture = None
        self.thread = None


camera = Camera(camera_index=1)