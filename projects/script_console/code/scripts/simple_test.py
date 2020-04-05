import console, time

keys = console.Keypad()
display = console.Display()


def center_text(txt):
    """
    This function will center all incoming strings to a fix size of the display
    max_char property.

    Args:
        txt: String to be centered.

    Returns:
        type: String with the text centered
    """
    return '{: ^{}}'.format(txt, display.max_char)


display.print_on_line(center_text("Wujuuu imported"), 0)
display.print_on_line(center_text("Press the"), 3)
display.print_on_line(center_text("button 0 to"), 4)
display.print_on_line(center_text("count presses"), 5)

intCounter = 0

while True:
    buttons = keys.get_keypad()
    if buttons and buttons[3] == 0:
        intCounter += 1
        display.clear(0, 1)
        display.print_on_line(center_text("IT IS WORKING!!!"), 0)
        display.print_on_line(center_text("Button presses"), 3)
        display.print_on_line(center_text(str(intCounter)), 5)
        time.sleep_ms(250)
        if intCounter > 10:
            break
