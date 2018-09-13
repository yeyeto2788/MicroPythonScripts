import json, time, urandom, console

def get_random_question():
    with open("questions.json", "r") as questionsfile:
        questions = json.loads(questionsfile.read())
    questionsfile.close()

    choise = urandom.getrandbits(5)
    return questions[str(choise)]

keyboard = console.Keypad()
oled = console.Display()
oled.clear(1, 1)
time.sleep(0.2)
oled.clear(0, 1)
oled.print_wrapped(get_random_question())

while True:
    buttons = keyboard.get_keypad()
    if buttons[2] == 0:
        oled.clear(0, 1)
        oled.print_wrapped(get_random_question())
    elif buttons[2] == 0 and buttons[3] == 0:
        raise console.ConsoleError
    time.sleep(1)
