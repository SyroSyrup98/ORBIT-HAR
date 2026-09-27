from pathlib import Path
import csv
import time


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_DIR = (
    PROJECT_ROOT
    / "data"
    / "actions"
)


class ActionRecorder:

    def __init__(self):

        DATASET_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )


    def save_sequence(
        self,
        action,
        sequence,
    ):

        if not sequence:
            return None


        # ----------------------------------------------------
        # UNIQUE SEQUENCE ID
        # ----------------------------------------------------

        sequence_id = time.strftime(
            "%Y%m%d_%H%M%S"
        )


        # ----------------------------------------------------
        # ACTION DIRECTORY
        # ----------------------------------------------------

        action_dir = (
            DATASET_DIR
            / action
        )

        action_dir.mkdir(
            parents=True,
            exist_ok=True,
        )


        # ----------------------------------------------------
        # CSV FILE
        # ----------------------------------------------------

        filename = (
            f"{action}_{sequence_id}.csv"
        )

        path = (
            action_dir
            / filename
        )


        # ----------------------------------------------------
        # FEATURE NAMES
        # ----------------------------------------------------

        feature_names = list(
            sequence[0].keys()
        )


        # ----------------------------------------------------
        # WRITE CSV
        # ----------------------------------------------------

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)


            # Header

            writer.writerow(
                [
                    "action",
                    "sequence_id",
                    "frame_index",
                    *feature_names,
                ]
            )


            # Feature rows

            for frame_index, features in enumerate(
                sequence
            ):

                writer.writerow(
                    [
                        action,
                        sequence_id,
                        frame_index,

                        *[
                            features.get(
                                name,
                                "",
                            )
                            for name in feature_names
                        ],
                    ]
                )


        print(
            f"Saved action sequence: {path}"
        )


        return path