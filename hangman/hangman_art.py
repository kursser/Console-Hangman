from art import stages
class HangmanRender:
    def __init__(self):
        self._stages = stages

    def get_three_attempts(self):
        return self._stages[0]

    def get_six_attempts(self):
        return self._stages[1]

    def get_ten_attempts(self):
        return self._stages[2]

