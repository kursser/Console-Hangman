from ui.ui_hangman import stages


def get_hangman(attempts):
    dict_stages = {3: stages[0], 6: stages[1], 10: stages[2]}
    return dict_stages[attempts]

# class HangmanRender:
#     def __init__(self):
#         self._stages = {3: stages[0], 6: stages[1], 10: stages[2]}
#
#     def get(self, attempts):
#         return self._stages[attempts]


