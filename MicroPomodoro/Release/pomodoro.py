import time
import json
import machine
import neopixel

try:
    import ssd1306
    blndisplay = True
except ImportError as error:
    print("Seems like there is no such module", error)
    blndisplay = False

def display_msg(message, line, start=0, show=0):
    lines = [0, 8, 16, 24, 32, 40, 48]
    if line in lines:
        display.text(message, start, line)
    if show:
        display.show()

def clear_display(fill=0, show=0):
    display.fill(fill)
    if show:
        display.show()

def print_text(text):
    clear_display()
    fill_amount = 16
    display_msg("*" * fill_amount, 24, 0, 1)
    display_msg('{:*^16}'.format(text), 32, 0, 1)
    display_msg("*" * fill_amount, 40, 0, 1)
    time.sleep(1)
    clear_display(0, 1)

def lapse_time(minutes, color, message=''):
    t_mins = minutes - 1
    for mins in range(t_mins, -1, -1):
        for secs in range(60, 0, -1):
            data = '{:02d} : {:02d}'.format(mins, secs)
            print("Remaining time:", data)
            for milisecs in range(40, 0, -1):
                set_pixel_color(milisecs % 12, color)
                time.sleep_ms(25)
            if blndisplay:
                clear_display()
                display_msg(data, 24, 32)
                display_msg('{:^16}'.format(message), 0)
                display.show()

def set_pixel_color(neopixel, color):
    if neostrip[neopixel] != (0, 0, 0):
        neostrip[neopixel] = (0, 0, 0)
    else:
        if color in config['colors']:
            neostrip[neopixel] = config['colors'][color]
    neostrip.write()

def color_neostrip(neostrip, color, pixel_count):
    if color in config['colors']:
        for intcounter in range(pixel_count):
            neostrip[intcounter] = config['colors'][color]
    neostrip.write()

def clear_neostrip(neostrip):
    neostrip.fill = (config['colors']['nocolor'])
    neostrip.write()

def load_config():
    with open("./config.json", "r") as conf_file:
        return json.load(conf_file)

config = load_config()

if blndisplay:
    try:
        i2c = machine.I2C(scl=machine.Pin(config['screen']['sda']), sda=machine.Pin(config['screen']['scl']))
        display = ssd1306.SSD1306_I2C(config['screen']['width'], config['screen']['height'], i2c)
        clear_display()
    except OSError:
        print("Error trying to initialize the code for the OLED")
        blndisplay = False

button = machine.Pin(config['button']['pin'], machine.Pin.IN, machine.Pin.PULL_UP)
PIXEL_COUNT = config['neopixel']['count']
neostrip = neopixel.NeoPixel(machine.Pin(config['neopixel']['pin']), PIXEL_COUNT)
clear_neostrip(neostrip)

while True:
    if (button.value() == 0):
        lapse_time(25, "red", "POMODORO")
        clear_neostrip(neostrip)
        lapse_time(5, "green", "FREE TIME")
        clear_neostrip(neostrip)
