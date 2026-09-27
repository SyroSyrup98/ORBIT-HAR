import math


class ObjectTracker:
    def __init__(self, movement_threshold=0.02):
        self.previous_objects = {}
        self.movement_threshold = movement_threshold

    def _center(self, bbox, frame_width, frame_height):
        x1, y1, x2, y2 = bbox

        return (
            ((x1 + x2) / 2) / frame_width,
            ((y1 + y2) / 2) / frame_height,
        )

    def _distance(self, a, b):
        return math.sqrt(
            (a[0] - b[0]) ** 2
            + (a[1] - b[1]) ** 2
        )

    def update(self, detections, frame_width, frame_height):
        current_objects = {}

        movement_features = {
            "object_moving": False,
            "object_speed": 0.0,
            "tracked_object": None,
        }

        for detection in detections:
            class_name = detection["class_name"]

            center = self._center(
                detection["bbox"],
                frame_width,
                frame_height,
            )

            previous = self.previous_objects.get(
                class_name
            )

            movement = 0.0

            if previous is not None:
                movement = self._distance(
                    center,
                    previous,
                )

            current_objects[class_name] = center

            if movement > movement_features["object_speed"]:
                movement_features["object_speed"] = movement
                movement_features["tracked_object"] = class_name

        movement_features["object_moving"] = (
            movement_features["object_speed"]
            >= self.movement_threshold
        )

        self.previous_objects = current_objects

        return movement_features