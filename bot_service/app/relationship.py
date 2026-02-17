class Relationship:
    def __init__(self):
        self.trust: float = 0.5
        self.anger: float = 0.0
        self.respect: float = 0.5

    def to_dict(self):
        return {
            "trust": self.trust,
            "anger": self.anger,
            "respect": self.respect
        }