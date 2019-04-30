from console import Display
import time

images = ["/img/erni_l.txt", "/img/erni_s.txt", "/img/erni_logo.txt", "/img/github_logo.txt",
          "/img/upython_logo.txt", "/img/python_logo.txt", "/img/upython_logo_s.txt",
          "/img/MSC_logo.txt"]


def show():
    
    oled = Display()

    for image in images:
        oled.clear(0, 1)
        oled.draw_graphic(image, 35, 2)
        time.sleep(5)


show()
