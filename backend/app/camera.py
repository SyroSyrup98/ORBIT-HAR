import cv2


class Camera:
    def __init__(self, camera_index=1):
        self.camera_index = camera_index
        self.capture = None

    def start(self):
        if self.capture is None:
            self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            raise RuntimeError("Could not open camera")

    def read(self):
        if self.capture is None:
            self.start()

        success, frame = self.capture.read()

        if not success:
            raise RuntimeError("Could not read camera frame")

        return frame

    def stop(self):
        if self.capture is not None:
            self.capture.release()
            self.capture = None


camera = Camera()