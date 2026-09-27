import math


def point_to_bbox_distance(point, bbox):
    """
    Minimum normalized distance from a point to a bounding box.

    point:
        {"x": ..., "y": ...} in normalized coordinates (0-1)

    bbox:
        [x1, y1, x2, y2] in pixel coordinates
    """

    px = point["x"]
    py = point["y"]

    x1, y1, x2, y2 = bbox

    return {
        "x": px,
        "y": py,
    }


def bbox_center(bbox, frame_width, frame_height):
    x1, y1, x2, y2 = bbox

    return {
        "x": ((x1 + x2) / 2) / frame_width,
        "y": ((y1 + y2) / 2) / frame_height,
    }


def bbox_size(bbox, frame_width, frame_height):
    x1, y1, x2, y2 = bbox

    width = (x2 - x1) / frame_width
    height = (y2 - y1) / frame_height

    return width, height


def point_inside_bbox(point, bbox, frame_width, frame_height):
    x1, y1, x2, y2 = bbox

    px = point["x"] * frame_width
    py = point["y"] * frame_height

    return (
        x1 <= px <= x2
        and y1 <= py <= y2
    )


def distance_between_points(a, b):
    return math.sqrt(
        (a["x"] - b["x"]) ** 2
        + (a["y"] - b["y"]) ** 2
    )


def analyze_hand_object_interaction(
    landmarks,
    detections,
    frame_width,
    frame_height,
):
    """
    Analyze the relationship between wrists and detected objects.

    Returns interaction features for the current frame.
    """

    if not landmarks:
        return {
            "left_hand_object_distance": None,
            "right_hand_object_distance": None,
            "left_hand_near_object": False,
            "right_hand_near_object": False,
            "left_hand_holding": False,
            "right_hand_holding": False,
        }

    left_wrist = landmarks[15]
    right_wrist = landmarks[16]

    result = {
        "left_hand_object_distance": None,
        "right_hand_object_distance": None,

        "left_hand_near_object": False,
        "right_hand_near_object": False,

        "left_hand_holding": False,
        "right_hand_holding": False,
    }

    if not detections:
        return result

    # Use the closest detected object to either wrist.
    for detection in detections:

        bbox = detection["bbox"]

        object_center = bbox_center(
            bbox,
            frame_width,
            frame_height,
        )

        left_distance = distance_between_points(
            left_wrist,
            object_center,
        )

        right_distance = distance_between_points(
            right_wrist,
            object_center,
        )

        if (
            result["left_hand_object_distance"] is None
            or left_distance
            < result["left_hand_object_distance"]
        ):
            result["left_hand_object_distance"] = left_distance

        if (
            result["right_hand_object_distance"] is None
            or right_distance
            < result["right_hand_object_distance"]
        ):
            result["right_hand_object_distance"] = right_distance

        # Normalized proximity threshold.
        if left_distance < 0.12:
            result["left_hand_near_object"] = True

        if right_distance < 0.12:
            result["right_hand_near_object"] = True

        # Wrist inside object bounding box.
        if point_inside_bbox(
            left_wrist,
            bbox,
            frame_width,
            frame_height,
        ):
            result["left_hand_holding"] = True

        if point_inside_bbox(
            right_wrist,
            bbox,
            frame_width,
            frame_height,
        ):
            result["right_hand_holding"] = True

    return result