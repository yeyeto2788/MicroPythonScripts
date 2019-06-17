import time
import os
import sys
import console

keys = console.Keypad()
oled = console.Display()

def print_menu(words):
    if isinstance(words, list) and len(words) <= 8:
        line = 0
        for script in words:
            if line > len(oled.v_lines):
                time.sleep(2)
                line = 0
            oled.print_on_line(str(script), line)
            line += 1
    else:
        oled.print_wrapped(words)
    time.sleep(1)

def print_selection(scripts, selection):
    oled.clear(0, 1)
    oled.print_on_line("Script selected:" + str(selection), 1)
    oled.print_on_line(str(scripts[selection]), 2)
    oled.draw_rect(0, oled.v_lines[2], oled.width, oled.char_width)
    oled.draw_rect_filled(oled.width - oled.char_width, oled.v_lines[2], oled.char_width, oled.char_width)

def get_files():
    extensions = ".py"
    excluded_files = ["main.py", "boot.py", "console.py", __name__]
    dirfiles = []
    for filename in os.listdir(os.getcwd()):
        if filename.lower().endswith(extensions):
            if filename.lower() not in excluded_files:
                dirfiles.append(filename.replace(extensions, ""))
    return dirfiles

scripts = get_files()
selection = 0
while True:
    start_time = time.ticks_ms() // 1000
    console_idle = 0
    oled.clear(0, 1)
    print_menu(scripts[0:len(oled.v_lines)])
    while True:
        time_now = time.ticks_ms() // 1000
        buttons = keys.get_keypad()
        btnUp = buttons[0]
        btnDown = buttons[1]
        btnSelect = buttons[2]
        btnStart = buttons[3]
        if buttons and btnDown == 0:
            try:
                start_time = time.ticks_ms() // 1000
                selection += 1
                if selection > (len(scripts) - 1):
                    selection = 0
                print_selection(scripts, selection)
                console_idle = 0
            except:
                pass
        elif buttons and btnUp == 0:
            try:
                start_time = time.ticks_ms() // 1000
                selection -= 1
                if selection < 0:
                    selection = len(scripts) - 1
                print_selection(scripts, selection)
                console_idle = 0
            except:
                pass
        elif buttons and btnStart == 0:
            start_time = time.ticks_ms() // 1000
            try:
                __import__(scripts[selection])
            except console.ConsoleError:
                oled.clear(0, 1)
                oled.print_wrapped("Going back to main menu.")
                time.sleep(0.5)
                continue
            del sys.modules[scripts[selection]]

        if (time_now - start_time) > (3 * 60):
            if not console_idle:
                oled.clear(0, 1)
                oled.print_on_line(" TIME IS OUT!!! ", 1)
                oled.print_on_line("Shutting off the", 5)
                oled.print_on_line("     screen     ", 6)
                time.sleep(2)
                oled.clear(0, 1)
                console_idle = 1
        elif (time_now - start_time) > 5:
            if not console_idle:
                start_time = time.ticks_ms() // 1000
                selection += 1
                if selection > (len(scripts) - 1):
                    selection = 0
                print_selection(scripts, selection)
        time.sleep(0.1)
    del scripts
    time.sleep(0.1)
