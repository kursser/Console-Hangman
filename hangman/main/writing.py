from time import sleep

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