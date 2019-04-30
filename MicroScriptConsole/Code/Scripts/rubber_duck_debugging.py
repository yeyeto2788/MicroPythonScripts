import time
import urandom
from console import Display, Button

oled = Display()
buttonSelect = Button(0)

questions = ["Which person around you could help you?",
             "Maybe you should consider refactoring?",
             "Have you tried step by step execution?",
             "Maybe some threads are unnecessary?",
             "Maybe you turn it off and on again?",
             "Could there be some race condition?",
             "Where is the lacking print()?",
             "Have you talked to your colleague?",
             "Why not call for a group meeting?",
             "Why not walk around your office?",
             "Should you really be doing this?",
             "Can the problem be broken down?",
             "Have you tried to unit test it?",
             "Maybe it is time for a coffee?",
             "Have you tried a clean build?",
             "Can you give me more details?",
             "Can this be hardware related?",
             "Could this not be your fault?",
             "Is this actually a problem?",
             "Can the code be simplified?",
             "Have you tried googling it?",
             "Maybe you can turn it on and off?",
             "I am not sure try again!",
             "Try again after having a coffee!",
             "Walk around the office and try again!",
             "Have you tried pair programming this?",
             "Maybe some of the threads are unnecessary?",
             "Can the problem be broken down more?",
             "Call for a group meeting to discuss this!",
             "Maybe you should consider some refactoring!",
             "Have you tried googling it?",
             "Why not try it again?"]


def get_random_str(items):
    """
    Select a seudo-random string from a given list.

    Args:
        items (lst): List from where to select item.

    Returns:
        item selected value.
    """
    choise = urandom.getrandbits(5)
    try:
        s_return = items[choise]
        return s_return
    except IndexError:
        return get_random_str(items)


def main():
    oled.clear(1, 1)
    time.sleep(0.2)
    oled.clear(0, 1)

    while True:
        if not buttonSelect.isReleased():
            oled.clear(0, 1)
            time.sleep(1)
            oled.print_wrapped(get_random_str(questions))

main()