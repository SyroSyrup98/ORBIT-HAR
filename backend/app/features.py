import math


def distance(a, b):
    """
    Euclidean distance between two 3D landmarks.
    """

    return math.sqrt(
        (a["x"] - b["x"]) ** 2
        + (a["y"] - b["y"]) ** 2
        + (a["z"] - b["z"]) ** 2
    )


def angle(a, b, c):
    """
    Angle ABC in degrees.
    """

    ba = (
        a["x"] - b["x"],
        a["y"] - b["y"],
        a["z"] - b["z"],
    )

    bc = (
        c["x"] - b["x"],
        c["y"] - b["y"],
        c["z"] - b["z"],
    )

    dot = (
        ba[0] * bc[0]
        + ba[1] * bc[1]
        + ba[2] * bc[2]
    )

    magnitude_ba = math.sqrt(
        ba[0] ** 2
        + ba[1] ** 2
        + ba[2] ** 2
    )

    magnitude_bc = math.sqrt(
        bc[0] ** 2
        + bc[1] ** 2
        + bc[2] ** 2
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0.0

    cosine = dot / (magnitude_ba * magnitude_bc)

    cosine = max(-1.0, min(1.0, cosine))

    return math.degrees(math.acos(cosine))


def extract_features(landmarks):
    """
    Convert 33 pose landmarks into an interpretable
    feature dictionary.
    """

    if landmarks is None or len(landmarks) < 33:
        return None

    # MediaPipe Pose landmark indices
    NOSE = 0

    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12

    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14

    LEFT_WRIST = 15
    RIGHT_WRIST = 16

    LEFT_HIP = 23
    RIGHT_HIP = 24

    LEFT_KNEE = 25
    RIGHT_KNEE = 26

    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28

    features = {}

    # -------------------------
    # BODY SCALE
    # -------------------------

    shoulder_width = distance(
        landmarks[LEFT_SHOULDER],
        landmarks[RIGHT_SHOULDER],
    )

    hip_width = distance(
        landmarks[LEFT_HIP],
        landmarks[RIGHT_HIP],
    )

    features["shoulder_width"] = shoulder_width
    features["hip_width"] = hip_width


    # -------------------------
    # ELBOW ANGLES
    # -------------------------

    features["left_elbow_angle"] = angle(
        landmarks[LEFT_SHOULDER],
        landmarks[LEFT_ELBOW],
        landmarks[LEFT_WRIST],
    )

    features["right_elbow_angle"] = angle(
        landmarks[RIGHT_SHOULDER],
        landmarks[RIGHT_ELBOW],
        landmarks[RIGHT_WRIST],
    )


    # -------------------------
    # KNEE ANGLES
    # -------------------------

    features["left_knee_angle"] = angle(
        landmarks[LEFT_HIP],
        landmarks[LEFT_KNEE],
        landmarks[LEFT_ANKLE],
    )

    features["right_knee_angle"] = angle(
        landmarks[RIGHT_HIP],
        landmarks[RIGHT_KNEE],
        landmarks[RIGHT_ANKLE],
    )


    # -------------------------
    # WRIST POSITIONS
    # -------------------------

    features["left_wrist_x"] = landmarks[LEFT_WRIST]["x"]
    features["left_wrist_y"] = landmarks[LEFT_WRIST]["y"]
    features["left_wrist_z"] = landmarks[LEFT_WRIST]["z"]

    features["right_wrist_x"] = landmarks[RIGHT_WRIST]["x"]
    features["right_wrist_y"] = landmarks[RIGHT_WRIST]["y"]
    features["right_wrist_z"] = landmarks[RIGHT_WRIST]["z"]


    # -------------------------
    # WRIST → SHOULDER DISTANCES
    # -------------------------

    features["left_wrist_shoulder_distance"] = distance(
        landmarks[LEFT_WRIST],
        landmarks[LEFT_SHOULDER],
    )

    features["right_wrist_shoulder_distance"] = distance(
        landmarks[RIGHT_WRIST],
        landmarks[RIGHT_SHOULDER],
    )


    # -------------------------
    # HAND → HAND DISTANCE
    # -------------------------

    features["hand_distance"] = distance(
        landmarks[LEFT_WRIST],
        landmarks[RIGHT_WRIST],
    )


    # -------------------------
    # WRIST → TORSO
    # -------------------------

    torso_center = {
        "x": (
            landmarks[LEFT_SHOULDER]["x"]
            + landmarks[RIGHT_SHOULDER]["x"]
            + landmarks[LEFT_HIP]["x"]
            + landmarks[RIGHT_HIP]["x"]
        ) / 4,

        "y": (
            landmarks[LEFT_SHOULDER]["y"]
            + landmarks[RIGHT_SHOULDER]["y"]
            + landmarks[LEFT_HIP]["y"]
            + landmarks[RIGHT_HIP]["y"]
        ) / 4,

        "z": (
            landmarks[LEFT_SHOULDER]["z"]
            + landmarks[RIGHT_SHOULDER]["z"]
            + landmarks[LEFT_HIP]["z"]
            + landmarks[RIGHT_HIP]["z"]
        ) / 4,
    }

    features["left_wrist_torso_distance"] = distance(
        landmarks[LEFT_WRIST],
        torso_center,
    )

    features["right_wrist_torso_distance"] = distance(
        landmarks[RIGHT_WRIST],
        torso_center,
    )


    # -------------------------
    # LANDMARK VISIBILITY
    # -------------------------

    visible_count = sum(
        1
        for landmark in landmarks
        if landmark["visibility"] > 0.5
    )

    features["visible_landmarks"] = visible_count


    return features