import time
import urandom
from console import Display, Button

oled = Display()
buttonSelect = Button(0)

answers = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes, definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it"
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"]


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
    oled.print_wrapped("  Magic 8 Ball  ")
    time.sleep(1)

    while True:
        if not buttonSelect.is_released():
            oled.clear(0, 1)
            time.sleep(1)
            oled.print_wrapped(get_random_str(answers))


main()