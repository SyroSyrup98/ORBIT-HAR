class RecordingController:

    def __init__(self, sequence_length=30):
        self.sequence_length = sequence_length

        self.recording = False
        self.action = None
        self.sequence = []


    def start(self, action):
        if self.recording:
            return False

        self.action = action.upper()
        self.sequence = []
        self.recording = True

        print(
            f"Recording started: {self.action}"
        )

        return True


    def add_frame(self, features):
        if not self.recording:
            return False

        if features is None:
            return False

        self.sequence.append(
            features.copy()
        )

        if len(self.sequence) >= self.sequence_length:
            return True

        return False


    def is_complete(self):
        return (
            self.recording
            and len(self.sequence)
            >= self.sequence_length
        )


    def get_sequence(self):
        return self.sequence.copy()


    def reset(self):
        self.recording = False
        self.action = None
        self.sequence = []


    def progress(self):
        return {
            "recording": self.recording,
            "action": self.action,
            "frames": len(self.sequence),
            "target": self.sequence_length,
            "complete": self.is_complete(),
        }