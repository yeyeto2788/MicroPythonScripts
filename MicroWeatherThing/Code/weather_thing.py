import ssd1306
import json
import urequests
import time
import dht
import machine


def connect_wifi(ssid, pwd):
    """
    Function to connect to WIFI.

    Args:
        ssid: Name of the WIFI connection.
        pwd: Boolean for the connection.

    Returns: 
        True if it's connected to wifi

    """
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        display_msg('Connecting to network...', 8)
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    return True


def get_weather(city, api_key):
    """
    This gets the current weather from the OpenWeatherMap API

    Args:
        city: City you want the weather from
        api_key: api_key: API Key from OpenWeatherMap

    Returns:
        Data retrieved from the API.

    """
    r = urequests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s" % (city, api_key)
    ).json()
    data = []
    min_temp = int(r["main"]["temp_min"] - 273.15)
    data.append("Min: %s C" % min_temp)
    max_temp = int(r["main"]["temp_max"] - 273.15)
    data.append("Max: %s C" % max_temp)
    actual_temp = int(r["main"]["temp"] - 273.15)
    data.append("Current: %s C" % actual_temp)
    humidity = int(r["main"]["humidity"])
    data.append("Humidity: %s" % humidity)
    condition = str(r["weather"][0]["description"])
    data.append("Condition: %s" % condition)
    return data


def clear_display():
    """
    Display clear so no information will be shown.

    Returns:
        None.

    """
    display.fill(0)


def display_msg(message, line, start=0):
    """
    Display the message on the screen.

    Args:
        message: String with the text that wants to be shown
        line: Line where you want the text
        start: Integer where the text will start to be printed

    Returns:
        None.

    """
    lines = [0, 8, 16, 24, 32, 40, 48]
    if line in lines:
        display.text(message, start, line)


def draw_hline(x, y):
    """
    Draw a horizontal line on the screen

    Args:
        x: X pixel
        y: Y pixel

    Returns:
        None.

    """
    for i in range(0, x):
        display.pixel(i, y, 1)


def draw_vline(x, y):
    """
    Draw a vertical line on the screen

    Args:
        x: X pixel
        y: Y pixel

    Returns:
        None.

    """
    for i in range(0, y):
        display.pixel(x, i, 1)


def parse_weather_data(data):
    """
    Parse weather data from the GetWeather function and show the weather on the screen.

    Args:
        data: Array from the GetWeather function.

    Returns:
        None.

    """
    clear_display()
    for i in range(0, len(data)):
        if i < (len(data) - 1):
            display_msg(data[i], int(i * 8))
        else:
            final_line = data[i].split(": ")
            display_msg(final_line[0], 40)
            display_msg('{:^16}'.format(final_line[1]), 48)
            draw_hline(WIDTH, 37)
        display.show()


def get_time():
    """
    Get local time from the internet.

    Returns:
        String with the time

    """
    import ntptime
    ntptime.settime()
    ts = time.localtime()
    year = ts[0]
    month = ts[1]
    day = ts[2]
    hour = ts[3]
    mins = ts[4]
    actual_time = "%s/%s/%s %s:%s" % (str(day), str(month), str(year), str(hour), str(mins))
    return actual_time


def show_time():
    """
    This function will show the time on the OLED shield

    Returns:
        None.

    """
    clear_display()
    display_msg('{:^16}'.format("CLOCK"), 8)
    data = get_time().split(" ")
    display_msg('{:^16}'.format(data[0]), 32)
    display_msg('{:^16}'.format(data[1]), 40)
    display.show()


def get_local_conditions():
    """
    This will get the time from the internet if the internet connection
    NOTE: take into account that this can give a time from the server which can be in other
    location.

    Returns:
        None.

    """
    clear_display()
    d = dht.DHT11(machine.Pin(4))
    display_msg('{:16}'.format("Local Temp:"), 16)
    display_msg('{:^16}'.format(str(d.temperature())), 24)
    display_msg('{:16}'.format("Local Humidity:"), 40)
    display_msg('{:^16}'.format(str(d.humidity())), 48)
    display.show()


i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
WIDTH = 128
HEIGHT = 64
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

CITY = 'City you want the weather from'
API_KEY = 'OpenWeatherAPI'
SSID = 'Name of the WIFI connection'
PWD = 'Wifi connection password'

received_data = get_weather(CITY, API_KEY)
start_time = time.ticks_ms() // 1000

while connect_wifi(SSID, PWD):
    time_now = time.ticks_ms() // 1000

    if (time_now - start_time) < (3 * 60):
        show_time()
        time.sleep(30)
        get_local_conditions()
        time.sleep(30)
        parse_weather_data(received_data)
        time.sleep(30)
    else:
        received_data = get_weather(CITY, API_KEY)
        start_time = time.ticks_ms() // 1000
