class ActionRecognizer:

    def __init__(self):
        self.previous_object_moving = False
        self.previous_object_speed = 0.0
        self.previous_hand_distance = None

    def recognize(self, features):

        if features is None:
            return self._result(
                "UNKNOWN",
                0.0,
                "No features available",
            )

        left_distance = features.get(
            "left_hand_object_distance"
        )

        right_distance = features.get(
            "right_hand_object_distance"
        )

        left_near = features.get(
            "left_hand_near_object",
            False,
        )

        right_near = features.get(
            "right_hand_near_object",
            False,
        )

        object_moving = features.get(
            "object_moving",
            False,
        )

        object_speed = features.get(
            "object_speed",
            0.0,
        )

        distances = [
            d
            for d in (
                left_distance,
                right_distance,
            )
            if d is not None
        ]

        closest_distance = (
            min(distances)
            if distances
            else None
        )

        hand_near = (
            left_near
            or right_near
        )

        # ----------------------------------------------------
        # Determine whether the object has just started moving
        # ----------------------------------------------------

        object_started_moving = (
            object_moving
            and not self.previous_object_moving
        )

        # ----------------------------------------------------
        # Determine whether the object has just stopped
        # ----------------------------------------------------

        object_stopped = (
            not object_moving
            and self.previous_object_moving
        )

        # ====================================================
        # PICK UP
        # ====================================================

        if (
            hand_near
            and object_started_moving
        ):

            result = self._result(
                "PICK_UP",
                0.90,
                "Hand near object and object movement started",
            )

            self._update(
                object_moving,
                object_speed,
                closest_distance,
            )

            return result

        # ====================================================
        # MOVE
        # ====================================================

        if (
            hand_near
            and object_moving
            and object_speed >= 0.02
        ):

            result = self._result(
                "MOVE",
                0.90,
                "Object moving while hand remains near object",
            )

            self._update(
                object_moving,
                object_speed,
                closest_distance,
            )

            return result

        # ====================================================
        # PLACE
        # ====================================================

        if (
            object_stopped
            and not hand_near
        ):

            result = self._result(
                "PLACE",
                0.85,
                "Object movement stopped and hand separated",
            )

            self._update(
                object_moving,
                object_speed,
                closest_distance,
            )

            return result

        # ====================================================
        # REACH
        # ====================================================

        if (
            closest_distance is not None
            and closest_distance < 0.25
            and not hand_near
            and not object_moving
        ):

            result = self._result(
                "REACH",
                0.75,
                "Hand approaching detected object",
            )

            self._update(
                object_moving,
                object_speed,
                closest_distance,
            )

            return result

        # ====================================================
        # UNKNOWN
        # ====================================================

        result = self._result(
            "UNKNOWN",
            0.0,
            "No action condition satisfied",
        )

        self._update(
            object_moving,
            object_speed,
            closest_distance,
        )

        return result

    def _update(
        self,
        object_moving,
        object_speed,
        hand_distance,
    ):
        self.previous_object_moving = object_moving
        self.previous_object_speed = object_speed
        self.previous_hand_distance = hand_distance

    def _result(
        self,
        action,
        confidence,
        reason,
    ):
        return {
            "action": action,
            "confidence": confidence,
            "reason": reason,
        }