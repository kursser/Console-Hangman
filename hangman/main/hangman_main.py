from writing import write
from random import choice
import json
from ui.get_hangman import get_hangman
from ui import ui_text
import sys



class HangmanGame():

    _ALPHABET = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у",
                "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]


    def __init__(self):
        self._all_words = self._load_words()
        self._attempts = None
        self._category = self._pick_category()
        self._word = self._pick_word()
        self._word_completion = ["_"] * len(self._word)  # строка, содержащая символы _ на каждую букву задуманного слова
        self._guessed_letters = [] # список уже названных букв
        self._guessed_words = [] # список уже названных слов
        self._cnt_attempts = 1 # cчётчик попыток
        self._hangman = None
        self._draw_hangman = None



    def _load_words(self):
        with open('../words.json', 'r', encoding='utf-8') as dict_words:
            return json.load(dict_words)


    def _pick_category(self):
        category = choice(list(self._all_words))
        return category


    def _pick_word(self):
        return choice(self._all_words[self._category])


    def _update_data(self):
        self._category = self._pick_category()
        self._word = self._pick_word()
        self._word_completion = ["_"] * len(self._word)
        self._cnt_attempts = 1
        self._guessed_letters = []
        self._guessed_words = []




    @staticmethod
    def _validate_selection_in_menu(selection):

        if selection not in ('1', '2', '3'):
            raise ValueError('Неверная операция, повторите попытку')

        elif selection == '1':
            return 'play'

        elif selection == '2':
            return 'instruction'

        elif selection == '3':
            return 'exit'


    def _difficulty_selection(self, selection):
        if selection not in ('1', '2', '3'):
            raise ValueError('Неверная операция, повторите попытку')

        elif selection == '1':
            self._attempts = 10

        elif selection == '2':
            self._attempts = 6

        elif selection == '3':
            self._attempts = 3


    @staticmethod
    def _play_again(answer):
        answer = answer.lower()
        if answer not in ('y', 'yes', 'да', 'д', 'no', 'n', 'нет', 'н'):
            raise ValueError('Некорректная команда')

        elif answer in ('y', 'yes', 'да', 'д'):
            return True

        elif answer in ('no', 'n', 'нет', 'н'):
            return False

    def _guess_letter(self, letter):
        if letter in self._guessed_letters:
            raise ValueError('Вы уже использовали такую букву')

        elif letter not in self._ALPHABET:
            raise ValueError('Некорректный ввод!!! Повторите попытку')

        elif letter in self._word:
            self._guessed_letters.append(letter)
            for index, i in enumerate(self._word):
                if letter == i:
                    self._word_completion[index] = i.upper()
            return 'correct'


        elif letter not in self._word:
            self._guessed_letters.append(letter)
            self._cnt_attempts += 1
            return 'wrong'


    def _guess_word(self, g_word):
        # YA tyt dumayu
        if g_word in self._guessed_words:
            raise ValueError('Вы уже пытались использовать такое слово')

        elif len(g_word) != len(self._word):
            raise ValueError('Некорректный ввод. Загаданное слово должно быть длиннее. Повторите попытку!!')


        elif len(g_word) == len(self._word):
            if g_word != self._word and all(map(lambda x: x in self._ALPHABET, g_word)):
                self._guessed_words.append(g_word)
                self._cnt_attempts += 1
                return 'wrong'

            elif g_word == self._word:
                return 'win'

            else:
                raise ValueError('Некорректный ввод!!! Повторите попытку')



    def _play(self):
            while True:
                print(ui_text.difficulty_selection)
                try:
                    selection = input()
                    self._difficulty_selection(selection)
                    self._hangman = get_hangman(self._attempts)
                    break
                except ValueError as er:
                    write(str(er))
                    continue

            while self._cnt_attempts <= self._attempts + 1:

                self._draw_hangman = self._hangman[self._cnt_attempts - 1]

                print(self._draw_hangman)

                print("Посмотрите наверх, это вы!!!")
                print()
                print(f"\t| Категория {self._category.capitalize()} |")

                print(
                    self._cnt_attempts,
                    f"                <== это номер вашей попытки (максимум {self._attempts})",
                )
                print(
                    *self._word_completion,
                    f"        <== это загаданное слово из {len(self._word_completion)} букв",
                )
                print(self._guessed_letters, "               <== список уже названных букв")
                print(self._guessed_words, "               <== список уже названных слов")

                try:
                    write("Введите букву: ")

                    value = input().lower()

                    if len(value) == 1:
                        letter = value
                        state = self._guess_letter(letter)
                        if state == 'correct':
                            write(f'Вы угадали!! Буква {letter.upper()} есть в этом слове')

                        elif state == 'wrong':
                            write(f'Вы не угадали!! Буквы {letter.upper()} нет в этом слов')

                    else:
                        word = value
                        state = self._guess_word(word)
                        if state == 'win':
                            write("Поздравляю! Вы выиграли!")
                            return

                        elif state == 'wrong':
                            write('Вы не угадали, это не загаданное слово!!')

                except ValueError as er:
                    write(str(er))
                    continue

                if self._cnt_attempts == self._attempts + 1:
                    self._is_lost = True
                    print(self._draw_hangman)
                    write(ui_text.loose)
                    write(f"Загаданное слово было: {self._word.upper()}")
                    return

                elif "_" not in self._word_completion:
                    write(f"Поздравляю вы выиграли! Зааданное слово {self._word.upper()}")
                    return




    def start(self):
        while True:
            print(ui_text.title)
            print(ui_text.main_menu)
            try:
                selection = input()
                selection = self._validate_selection_in_menu(selection)
            except ValueError as er:
                write(str(er))
                continue


            if selection == 'play':
                self._play()
                while True:
                    try:
                        print(ui_text.game_again)
                        pick = input()
                        answer = self._play_again(pick)
                        if answer == True:
                            self._update_data()
                            self._play()
                            continue

                        else:
                            write('Спасибо за игру, до скорых встреч')
                            self._update_data()
                            break

                    except ValueError as er:
                        write(str(er))
                        continue

            elif selection == 'instruction':
                print(ui_text.instruction)
                input('Нажмите Enter чтобы вернуться в меню')


            elif selection == 'exit':
                sys.exit()
