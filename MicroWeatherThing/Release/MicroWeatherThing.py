import ssd1306, json, urequests, time, dht, machine

def ConnectWifi(SSID, pwd):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, pwd)
        while not sta_if.isconnected():
            pass
    return True


def Getweather(CITY, API_KEY):
    r = urequests.get("http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s" % (CITY, API_KEY)).json()
    Data = []
    TemperatureMin = int(r["main"]["temp_min"] - 273.15)
    Data.append("Min: %s C" % TemperatureMin)
    TemperatureMax = int(r["main"]["temp_max"] - 273.15)
    Data.append("Max: %s C" % TemperatureMax)
    ActualTemp = int(r["main"]["temp"] - 273.15)
    Data.append("Current: %s C" % ActualTemp)
    Humidity = int(r["main"]["humidity"])
    Data.append("Humidity: %s" % Humidity)
    Condition = str(r["weather"][0]["description"])
    Data.append("Condition: %s" % Condition)
    return Data


def ClearDisplay():
    display.fill(0)


def DisplayMsg(pstrMessage, pintLine, pintStart=0):
    Line = [0, 8, 16, 24, 32, 40, 48]
    if pintLine in Line:
        display.text(pstrMessage, pintStart, pintLine)


def DrawHLine(pintX, pintY):
    for i in range(0, pintX):
        display.pixel(i, pintY, 1)


def DrawVLine(pintX, pintY):
    for i in range(0, pintY):
        display.pixel(pintX, i, 1)


def ParseWeatherData(parrData):
    ClearDisplay()
    for i in range(0, len(parrData)):
        if i < (len(parrData) - 1):
            DisplayMsg(parrData[i], int(i * 8))
        else:
            FinalLine = parrData[i].split(": ")
            DisplayMsg(FinalLine[0], 40)
            DisplayMsg('{:^16}'.format(FinalLine[1]), 48)
            DrawHLine(Width, 37)
        display.show()


def GetTime():
    import ntptime
    ntptime.settime()
    ts = time.localtime()
    year = ts[0]
    Month = ts[1]
    day = ts[2]
    hour = ts[3]
    mins = ts[4]
    dayYear = ts[7]
    ActualTime = "%s/%s/%s %s:%s" % (str(day), str(Month), str(year), str(hour), str(mins))
    return ActualTime


def ShowTime():
    ClearDisplay()
    DisplayMsg('{:^16}'.format("CLOCK"), 8)
    strData = GetTime().split(" ")
    DisplayMsg('{:^16}'.format(strData[0]), 32)
    DisplayMsg('{:^16}'.format(strData[1]), 40)
    display.show()


def GetLocalTH():
    ClearDisplay()
    d = dht.DHT11(machine.Pin(4))
    DisplayMsg('{:16}'.format("Local Temp:"), 16)
    DisplayMsg('{:^16}'.format(str(d.temperature())), 24)
    DisplayMsg('{:16}'.format("Local Humidity:"), 40)
    DisplayMsg('{:^16}'.format(str(d.humidity())), 48)
    display.show()


i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
Width = 128
Height = 64
display = ssd1306.SSD1306_I2C(Width, Height, i2c)

CITY = 'City you want the weather from'
API_KEY = 'OpenWeatherAPI'
SSID = 'Name of the WIFI connection'
pwd = 'Wifi connection password'

ReceivedData = Getweather(CITY, API_KEY)
start_time = time.ticks_ms() // 1000

while ConnectWifi(SSID, pwd):
    time_now = time.ticks_ms() // 1000

    if (time_now - start_time) < (3 * 60):
        ShowTime()
        time.sleep(30)
        GetLocalTH()
        time.sleep(30)
        ParseWeatherData(ReceivedData)
        time.sleep(30)
    else:
        ReceivedData = Getweather(CITY, API_KEY)
        start_time = time.ticks_ms() // 1000
