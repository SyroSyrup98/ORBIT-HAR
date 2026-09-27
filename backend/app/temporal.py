from collections import deque


class TemporalBuffer:
    def __init__(self, max_length=30):
        self.buffer = deque(maxlen=max_length)

    def add(self, features):
        if features is None:
            return

        self.buffer.append(features)

    def get(self):
        return list(self.buffer)

    def clear(self):
        self.buffer.clear()

    def is_ready(self):
        return len(self.buffer) == self.buffer.maxlen

    def __len__(self):
        return len(self.buffer)