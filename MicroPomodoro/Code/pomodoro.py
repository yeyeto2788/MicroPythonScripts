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
    """
    Display a message on the OLED screen
    
    Args:
        message: String with the data to be written on the OLED screen.
        line: Integer of vertical pixel on which the pstrMessage will be written.
        start: Integer of horizontal pixel where it will start to write the pstrMessage
        show:

    Returns:
        None.
    """
    lines = [0, 8, 16, 24, 32, 40, 48]
    if line in lines:
        display.text(message, start, line)
    if show:
        display.show()


def clear_display(fill=0, show=0):
    """
    This can be use either to clear the screen will all pixels activated or deactivated by changing
    the blnFill and if the show is set to one it will immediately shown on the OLED screen
    
    Args:
        fill: Boolean to fill the screen.
        show: Boolean to show or not on the screen.

    Returns:
        None.
    """
    display.fill(fill)
    if show:
        display.show()


def print_text(text):
    """
    This will print a text center on the OLED screen.
    
    Args:
        text: String with data to show.

    Returns:
        None.
    """
    clear_display()
    fill_amount = 16
    display_msg("*" * fill_amount, 24, 0, 1)
    display_msg('{:*^16}'.format(text), 32, 0, 1)
    display_msg("*" * fill_amount, 40, 0, 1)
    time.sleep(1)
    clear_display(0, 1)


def lapse_time(minutes, color, message=''):
    """
    Countdown timer to execute on the code that will use other functions to clear the display
    add other data like string on the screen with the countdown timer.
    
    If no message it will not show anything but the countdown timer.
    
    Args:
        minutes: Integer with the amount of minutes to set the timer.
        message: String with the data to be shown on the OLED screen.

    Returns:
        None.
    """
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
    """

    Args:
        neopixel: Pixel to be fill with color.
        color: String with color to be filled.

    Returns:
        None.
    """
    if neostrip[neopixel] != (0, 0, 0):
        neostrip[neopixel] = (0, 0, 0)
    else:
        if color in config['colors']:
            neostrip[neopixel] = config['colors'][color]
    neostrip.write()


def color_neostrip(neostrip, color, pixel_count):
    """
    Set a color to the neopixel.
    
    Args:
        neostrip: neostrip.
        color: String with the color to be shown on the Neopixel.
        pixel_count: Integer with the amount of the Neopixel that has the neostrip.

    Returns:
        None
    """
    if color in config['colors']:
        for intcounter in range(pixel_count):
            neostrip[intcounter] = config['colors'][color]
    neostrip.write()


def clear_neostrip(neostrip):
    """
    Shutdown the neostrip or set the value to 0 for all Neopixel on the neostrip.
    
    Args:
        neostrip: neostrip.

    Returns:
        None
    """
    neostrip.fill = (config['colors']['nocolor'])
    neostrip.write()


def load_config():
    """
    Load configuration from the config.json file.

    Returns:
        json object with configuration.
    """
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
        # Add animation here
        # time.sleep_ms(3000)
        # Clear neostrip
        lapse_time(25, "red", "POMODORO")
        clear_neostrip(neostrip)
        lapse_time(5, "green", "FREE TIME")
        clear_neostrip(neostrip)
