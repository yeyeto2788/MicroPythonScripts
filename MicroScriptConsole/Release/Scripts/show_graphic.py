from console import Display, ConsoleError
import time

def show():
    oled = Display()
    oled.clear(0, 1)
    oled.draw_graphic("erni_l.txt", 35, 2)
    time.sleep(5)
    oled.clear(0, 1)
    oled.draw_graphic("erni_s.txt", 45, 20)
    time.sleep(5)
    oled.clear(0, 1)
    oled.draw_graphic("erni_logo.txt", 5, 20)
    time.sleep(5)
    oled.clear(0, 1)
    oled.draw_graphic("github_logo.txt", 35, 0)
    time.sleep(5)
    oled.clear(0, 1)
    oled.draw_graphic("upython_logo.txt", 35, 0)
    time.sleep(5)
    oled.clear(0, 1)
    oled.draw_graphic("python_logo.txt", 45, 20)
    time.sleep(5)
    oled.clear(0, 1)
    oled.draw_graphic("upython_logo_s.txt", 45, 20)
    time.sleep(5)
    oled.clear(0, 1)
    oled.draw_graphic("MSC_logo.txt", 15, 2)
    time.sleep(5)
    oled.clear(0, 1)

show()
