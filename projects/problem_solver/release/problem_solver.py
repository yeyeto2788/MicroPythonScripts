import json
import time
import urandom
import ssd1306
import machine

def clear_display(fill=0, show=0):
    display.fill(fill)
    if show:
        display.show()

def wrapped_text(message, max_chars=16):
    words = message.split(" ")
    wordlines = []
    msg = ""
    for iteraction, word in enumerate(words):
        remaining_chars = max_chars - len(msg)
        if (len(msg + " " + word) <= remaining_chars) or ((len(word) + 1) <= remaining_chars):
            if iteraction == len(words) - 1:
                msg += word + " "
                wordlines.append(msg)
                break
            else:
                msg += word + " "
        else:
            if iteraction == len(words) - 1:
                wordlines.append(msg)
                msg = word + (" " * remaining_chars)
                wordlines.append(msg)
                break
            else:
                wordlines.append(msg)
                msg = word + " "
        if (len(msg) >= max_chars):
            wordlines.append(msg)
            msg = ""
    return wordlines

def print_wrapped(words):
    lines = [0, 8, 16, 24, 32, 40, 48]
    if len(words) <= len(lines):
        for item, message in enumerate(words):
            display.text(message, 0, lines[item])
            display.show()
    else:
        line_counter = 0
        for iteraction in range(len(words)):
            if iteraction >= len(lines):
                time.sleep(3)
                line_counter = 0
            display.text(words[iteraction], 0, lines[line_counter])
            display.show()
            line_counter += 1

def get_random_question():
    with open("questions.json", "r") as q_file:
        questions = json.loads(q_file.read())
    q_file.close()

    choise = urandom.getrandbits(5)
    return questions[str(choise)]

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
clear_display()
clear_display(1, 1)
time.sleep_ms(100)
clear_display(0, 1)
print_wrapped(wrapped_text(get_random_question()))
time.sleep(5)
clear_display(1, 1)
time.sleep_ms(200)
clear_display(0, 1)
