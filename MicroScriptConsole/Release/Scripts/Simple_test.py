import console, time

buttonSelect = console.Button(0)
display = console.Display()

def center_text(txt):
    return '{: ^{}}'.format(txt, display.max_char)

display.print_on_line(center_text("Wujuuu imported"), 0)
display.print_on_line(center_text("Press the"), 3)
display.print_on_line(center_text("button 0 to"), 4)
display.print_on_line(center_text("count presses"), 5)

intCounter = 0

while True:
    if not buttonSelect.isReleased():
        intCounter += 1
        display.clear(0, 1)
        display.print_on_line(center_text("IT IS WORKING!!!"), 0)
        display.print_on_line(center_text("Button presses"), 3)
        display.print_on_line(center_text(str(intCounter)), 5)
        time.sleep_ms(250)
