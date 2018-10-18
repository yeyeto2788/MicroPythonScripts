import console, time

def show():
    display = console.Display()
    display.print_on_line("Wujuuu imported", 0, 1)
    time.sleep(3)
    display.clear(0, 1)

show()
