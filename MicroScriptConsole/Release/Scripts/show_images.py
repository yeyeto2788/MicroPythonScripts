import time
import os
from console import Display


def show():
    
    oled = Display()

    available_img = [image for image in os.listdir() if image.endswith('.txt')]
    for image in available_img:
        oled.clear(0, 1)
        oled.draw_graphic(image, 35, 2)
        time.sleep(5)


show()
