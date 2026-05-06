from ui.ui_hangman import stages
class HangmanRender:
    def __init__(self):
        self._stages = {3: stages[0], 6: stages[1], 10: stages[2]}

    def get(self, attempts):
        return self._stages[attempts]


