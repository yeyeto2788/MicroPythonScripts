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

def display_msg(pstrMessage, pintLine, pintStart=0, blnShow=0):
    Line = [0, 8, 16, 24, 32, 40, 48]
    if pintLine in Line:
        display.text(pstrMessage, pintStart, pintLine)
    if blnShow:
        display.show()


def clear_display(blnFill=0, blnShow=0):
    display.fill(blnFill)
    if blnShow:
        display.show()


def print_text(pstrString):
    clear_display()
    FillAmount = 16
    display_msg("*" * FillAmount, 24, 0, 1)
    display_msg('{:*^16}'.format(pstrString), 32, 0, 1)
    display_msg("*" * FillAmount, 40, 0, 1)
    time.sleep(1)
    clear_display(0, 1)


def lapse_time(pintMins, pstrColor, pstrmsg=''):
    totalMins = pintMins - 1
    for Mins in range(totalMins, -1, -1):
        for Secs in range(60, 0, -1):
            Data = '{:02d} : {:02d}'.format(Mins, Secs)
            print("Remaining time:", Data)
            for milisecs in range(40, 0, -1):
                set_pixel_color(milisecs % 12, pstrColor)
                time.sleep_ms(25)
            if blndisplay:
                clear_display()
                display_msg(Data, 24, 32)
                display_msg('{:^16}'.format(pstrmsg), 0)
                display.show()


def set_pixel_color(intNeopixel, pstrColor):
    if neostrip[intNeopixel] != (0, 0, 0):
        neostrip[intNeopixel] = (0, 0, 0)
    else:
        if pstrColor in config['colors']:
            neostrip[intNeopixel] = config['colors'][pstrColor]
    neostrip.write()


def color_neostrip(neostrip, pstrColor, pintPixelCount):
    if pstrColor in config['colors']:
        for intcounter in range(pintPixelCount):
            neostrip[intcounter] = config['colors'][pstrColor]
    neostrip.write()


def clear_neostrip(neostrip):
    neostrip.fill = (config['colors']['nocolor'])
    neostrip.write()


def load_config():
    with open("./config.json", "r") as ConfigFile:
        return json.load(ConfigFile)


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
        # Add animation here
        # time.sleep_ms(3000)
        # Clear neostrip
        lapse_time(25, "red", "POMODORO")
        clear_neostrip(neostrip)
        lapse_time(5, "green", "FREE TIME")
        clear_neostrip(neostrip)
