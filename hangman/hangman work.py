from time import sleep
from random import choice
import json
from hangman_art import HangmanRender


RUSSIAN_ALPHABET = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"]
with open('words.json', 'r', encoding='utf-8') as dict_words:
    WORDS = json.load(dict_words)


def write(text):
    for i in text:
        print(i, end="", flush=True)
        sleep(0.03)
    print()


def slow_write(text):
    for i in text:
        print(i, end="", flush=True)
        sleep(0.2)
    print()


def title():
    title = f"""   
    {'█' * 50}
    █{' ' * 48}█
    █{' ' * 15}ИГРА «ВИСЕЛИЦА»{' ' * 18}█
    █{' ' * 15}GAME «HANDMAN»{' ' * 19}█
    █{' ' * 48}█
    {'█' * 50}  
    """
    print(title)


def instructions():

    welcome = f"""
   
    {'-' * 50}  
    📜 ИНСТРУКЦИЯ:
    • Случайным образом выбирается категория и слово из этой категории
    • Вводите русские буквы по одной
    • Можно угадать всё слово целиком, но если слово окажется неверным, то это считается как ошибка
    • Осторожно: каждая ошибка приближает поражение!
    • Цель: спасти человечка, угадав слово
    {'-' * 50}
    🎪 Удачи в игре!
    """

    write(welcome)
    input("Нажмите ENTER чтобы вернуться в меню...")


def exit_the_game():
    pass


def difficulty_selection():
    difficulty = f"""
    1. ✅ Лёгкий (10 попыток)
    2. ⚠️ Средний (6 попыток) 
    3. 👺 Сложный (3 попытки)
    """
    difficulty_dict = {"1": 10, "2": 6, "3": 3}

    while True:

        print(difficulty)
        choice = input("Выберите уровень сложности: ")

        if choice in ("1", "2", "3"):
            return difficulty_dict[choice]

        else:
            write("Неверная операция!! Повторите попытку")
            continue


def random_word(WORDS):

    random_cathegory = choice(list(WORDS))

    random_item = choice(WORDS[random_cathegory])

    return random_item, random_cathegory


def choice_draw_hangman(index):
    '''функция, которая возвращает список рисунков виселицы для выбранной сложности'''
    render = HangmanRender()
    art_hangmans = {3: render.get_three_attempts, 6: render.get_six_attempts, 10: render.get_ten_attempts}
    return art_hangmans[index]()


def game_again():
    write("Желаете ли вы продолжить игру?")
    write("Напишите 'YES' или 'Y' или 'ДА' или 'Д', если желаете продолжить игру")
    write("Напишите 'NO' или 'N' или 'НЕТ' или 'Н', если желаете вернуться в меню")
    while True:
        say = input().lower()
        if say in ("yes", "y", "да", "д"):
            return True

        elif say in ("no", "n", "нет", "н"):
            return False

        else:
            write("Некорректная команда!!")
            write(
                "Введите 'YES' или 'Y' или 'ДА' или 'Д', если желаете продолжить игру"
            )
            write(
                "Введите 'NO' или 'N' или 'НЕТ' или 'Н', если желаете вернуться в меню"
            )
            continue


def main_game():

    word, category = random_word(WORDS)
    word_completion = [
        "_" for _ in range(len(word))
    ]  # строка, содержащая символы _ на каждую букву задуманного слова
    guessed_letters = []  # список уже названных букв
    guessed_words = []  # список уже названных слов
    cnt_tries = 1  # попытки
    all_tries = difficulty_selection()
    draw_hangman = choice_draw_hangman(all_tries)

    while cnt_tries <= all_tries + 1:

        if "_" not in word_completion:
            write("Поздравляю! Вы выиграли!")
            break

        chel = draw_hangman[cnt_tries - 1]
        print(chel)

        if cnt_tries == all_tries + 1:
            slow_write("Ты... Проиграл..")
            slow_write("Прости... Ты мне правда нравился")
            write(f"Загаданное слово было: {word.upper()}")
            print()
            break

        print("Посмотрите наверх, это вы!!!")
        print()
        print(f"\t| Категория {category.capitalize()} |")

        print(
            cnt_tries,
            f"                <== это номер вашей попытки (максимум {all_tries})",
        )
        print(
            *word_completion,
            f"        <== это загаданное слово из {len(word_completion)} букв",
        )
        print(guessed_letters, "               <== список уже названных букв")
        print(guessed_words, "               <== список уже названных слов")

        write("Введите букву: ")

        letter = input().lower()

        if letter == "ё":
            letter = "e"

        if len(letter) == len(word):

            if letter != word and all(map(lambda x: x in RUSSIAN_ALPHABET, letter)):
                write("Вы не угадали, это не загаданное слово!!")
                guessed_words.append(letter)
                cnt_tries += 1

            elif letter == word:
                write(f"Поздравляю вы угадали слово {letter.upper()}!!!")
                break

            else:
                write("Некорректный ввод!!! Повторите попытку")

        elif letter in guessed_words:
            write("Вы уже пытались использовать такое слово: ")

        elif letter in guessed_letters:
            write("Вы уже писались использовать такую букву: ")

        elif letter not in RUSSIAN_ALPHABET:
            write("Некорректный ввод!!! Повторите попытку")

        elif len(letter) == 1 and letter not in word:
            write(f"Неверно!! Такой {letter.upper()} в этом слове нет :( ")
            guessed_letters.append(letter)
            cnt_tries += 1

        elif len(letter) == 1 and letter in word:
            write(f"Вы угадали!! Буква {letter.upper()} есть в загаданном слове!!")
            guessed_letters.append(letter)
            for index, i in enumerate(word):
                if letter == i:
                    word_completion[index] = i.upper()


def game_menu():
    main_menu = f"""
    1. 🕹️ Играть
    2. 📜 Инструкция
    3. 🚪 Выход
    """

    print(main_menu)

    while True:

        choice = input()

        if choice in ("1", "2", "3"):
            return choice

        else:
            write("Неверная операция!! Повторите попытку")


def start_game():

    title()

    while True:
        choice = game_menu()
        if choice == "1":
            while True:
                main_game()
                isagain = game_again()
                if isagain:
                    continue
                else:
                    break

        elif choice == "2":
            instructions()

        elif choice == "3":
            write("Выход из игры...")
            break


start_game()


# ДОБАВИТЬ ВОЗМОЖНОСТЬ ВЫБОРА КАТЕГОРИИ
