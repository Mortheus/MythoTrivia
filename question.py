class Question:
    def __init__(self, dict):
        for key, value in dict:
            setattr(self, key, value)
