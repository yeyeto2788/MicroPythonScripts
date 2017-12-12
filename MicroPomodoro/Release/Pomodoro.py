import ssd1306
import time
import machine
import neopixel


def DisplayMsg(pstrMessage, pintLine, pintStart=0, blnShow=0):
    Line = [0, 8, 16, 24, 32, 40, 48]
    if pintLine in Line:
        display.text(pstrMessage, pintStart, pintLine)
    if blnShow:
        display.show()

def ClearDisplay(blnFill=0, blnShow=0):
    display.fill(blnFill)
    if blnShow:
        display.show()

def PrintText(pstrString):
    ClearDisplay()
    FillAmount = 16
    DisplayMsg("*" * FillAmount, 24, 0, 1)
    DisplayMsg('{:*^16}'.format(pstrString), 32, 0, 1)
    DisplayMsg("*" * FillAmount, 40, 0, 1)
    time.sleep(1)
    ClearDisplay(0, 1)

def Lapsetime(pintMins, pstrmsg=''):
    totalMins = pintMins - 1
    for Mins in range(totalMins, -1, -1):
        for Secs in range(60, 0, -1):
            Data = '{:02d} : {:02d}'.format(Mins, Secs)
            ClearDisplay()
            DisplayMsg(Data, 24, 32)
            DisplayMsg('{:^16}'.format(pstrmsg), 0)
            display.show()
            time.sleep(1)

def SetNeoColor(NeoString, pstrColor, pintPixelCount):
    if pstrColor == "Red":
        for i in range(pintPixelCount):
            NeoString[i] = (255, 0, 0)
    if pstrColor == "Green":
        for i in range(pintPixelCount):
            NeoString[i] = (0, 255, 0)
    if pstrColor == "Blue":
        for i in range(pintPixelCount):
            NeoString[i] = (0, 0, 255)
    if pstrColor == "White":
        for i in range(pintPixelCount):
            NeoString[i] = (255, 255, 255)
    NeoString.write()

def ClearNeoPixel(NeoString):
    NeoString.fill = ((0, 0, 0))
    NeoString.write()

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
Width = 128
Height = 64
display = ssd1306.SSD1306_I2C(Width, Height, i2c)
button = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)

PIXEL_COUNT = 3
NeoString = neopixel.NeoPixel(machine.Pin(15), PIXEL_COUNT)

if (button.value() == 0):
    ClearDisplay()
    SetNeoColor(NeoString, "Red", PIXEL_COUNT)
    Lapsetime(25, "POMODORO")
    SetNeoColor(NeoString, "White", PIXEL_COUNT)
    PrintText("   DONE   ")
    ClearDisplay(1, 1)
    time.sleep_ms(250)
    SetNeoColor(NeoString, "Green", PIXEL_COUNT)
    Lapsetime(5, "FREE TIME")
    PrintText("   DONE   ")
    ClearNeoPixel(NeoString)
    ClearDisplay(0, 1)
