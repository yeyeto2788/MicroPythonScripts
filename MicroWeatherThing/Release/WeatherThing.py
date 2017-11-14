import ssd1306, json, urequests, time, dht
from machine import I2C, Pin

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
    Data.append("Humidity: %s C" % Humidity)
    Condition = str(r["weather"][0]["description"])
    Data.append("Condition: %s C" % Condition)
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
    for i in range(0, len(parrData)):
        if i < (len(parrData) - 1):
            DisplayMsg(parrData[i], int(i * 8))
        else:
            FinalLine = parrData[i].split(": ")
            DisplayMsg(FinalLine[0], 40)
            DisplayMsg(FinalLine[1].rstrip(" C"), 48)
            DrawHLine(Width, 37)


def GetTime():
    import ntptime
    ntptime.settime()
    ts = utime.localtime()
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
    DisplayMsg("CLOCK", 16, 50)
    strData = GetTime().split(" ")
    DisplayMsg(strData[0], 32, 48)
    DisplayMsg(strData[1], 32, 56)
    display.show()


def GetLocalTH():
    ClearDisplay()
    d = dht.DHT11(machine.Pin(4))
    LocalTemp = "Temp: " + str(d.temperature()) + " ºC"
    LocalHum = "Humidity: " + str(d.humidity())
    DisplayMsg(LocalTemp, 8)
    DisplayMsg(LocalHum, 8)


i2c = I2C(scl=Pin(4), sda=Pin(5))
Width = 128
Height = 64
display = ssd1306.SSD1306_I2C(Width, Height, i2c)
CITY = 'Barcelona'
API_KEY = '53dc40faa391cc7bc1de714ed574bf13'
SSID = 'Sant Cugat Green'
pwd = 'green196970'
Counter = 0
ReceivedData = Getweather(CITY, API_KEY)

while ConnectWifi(SSID, pwd):
    Counter = Counter + 1
    if Counter < 40:
        ShowTime()
        time.sleep(30)
        GetLocalTH()
        time.sleep(30)
        ParseWeatherData(ReceivedData)
        time.sleep(30)
    else:
        ReceivedData = Getweather(CITY, API_KEY)
        Counter = 0
