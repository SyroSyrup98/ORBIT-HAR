from datetime import datetime


class ExperimentState:

    def __init__(self):

        self.steps = [
            {
                "number": 1,
                "action": "REACH",
                "object": "BOTTLE",
            },
            {
                "number": 2,
                "action": "PICK_UP",
                "object": "BOTTLE",
            },
            {
                "number": 3,
                "action": "MOVE",
                "object": "BOTTLE",
            },
            {
                "number": 4,
                "action": "PLACE",
                "object": "TRAY",
            },
        ]

        self.current_index = 0

        self.status = "READY"

        self.last_detected_action = None

        self.last_confidence = 0.0

        self.last_message = "Waiting for experiment"

        self.last_timestamp = None


    # ========================================================
    # CURRENT STEP
    # ========================================================

    def current_step(self):

        if self.current_index >= len(self.steps):

            return None

        return self.steps[
            self.current_index
        ]


    # ========================================================
    # PROCESS DETECTED ACTION
    # ========================================================

    def process_action(
        self,
        action,
        confidence,
    ):

        self.last_detected_action = action

        self.last_confidence = confidence

        self.last_timestamp = (
            datetime.now().isoformat()
        )


        # ----------------------------------------------------
        # Experiment already completed
        # ----------------------------------------------------

        if self.current_index >= len(
            self.steps
        ):

            self.status = "COMPLETE"

            self.last_message = (
                "Experiment completed"
            )

            return self.get_state()


        # ----------------------------------------------------
        # Get expected step
        # ----------------------------------------------------

        step = self.current_step()

        expected_action = step[
            "action"
        ]


        # ====================================================
        # CORRECT ACTION
        # ====================================================

        if action == expected_action:

            self.status = "STEP_COMPLETE"

            self.last_message = (
                f"Step {step['number']} "
                f"complete: {action}"
            )

            self.current_index += 1


            # ------------------------------------------------
            # Check experiment completion
            # ------------------------------------------------

            if self.current_index >= len(
                self.steps
            ):

                self.status = "COMPLETE"

                self.last_message = (
                    "Experiment completed successfully"
                )


        # ====================================================
        # WRONG ACTION
        # ====================================================

        elif action != "UNKNOWN":

            self.status = "DEVIATION"

            self.last_message = (
                f"Expected {expected_action}, "
                f"detected {action}"
            )


        # ====================================================
        # UNKNOWN ACTION
        # ====================================================

        else:

            self.status = "WAITING"

            self.last_message = (
                f"Waiting for {expected_action}"
            )


        return self.get_state()


    # ========================================================
    # GET CURRENT EXPERIMENT STATE
    # ========================================================

    def get_state(self):

        step = self.current_step()


        if step is None:

            expected_action = None
            expected_object = None

        else:

            expected_action = step[
                "action"
            ]

            expected_object = step[
                "object"
            ]


        return {

            "status": self.status,

            "current_step": (
                self.current_index + 1
                if step is not None
                else len(self.steps)
            ),

            "total_steps": len(
                self.steps
            ),

            "expected_action": (
                expected_action
            ),

            "expected_object": (
                expected_object
            ),

            "detected_action": (
                self.last_detected_action
            ),

            "confidence": (
                self.last_confidence
            ),

            "message": (
                self.last_message
            ),

            "timestamp": (
                self.last_timestamp
            ),
        }


    # ========================================================
    # RESET EXPERIMENT
    # ========================================================

    def reset(self):

        self.current_index = 0

        self.status = "READY"

        self.last_detected_action = None

        self.last_confidence = 0.0

        self.last_message = (
            "Waiting for experiment"
        )

        self.last_timestamp = None

        return self.get_state()