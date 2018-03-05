from wittyUtils import WittyBoard
import time

witty = WittyBoard()


def toggle_led(intmins, strled):
    initvalue = 0
    initialTime = time.ticks_ms()
    itertime = initialTime
    witty.clear_leds()
    while ((time.ticks_ms() - initialTime) / 1000) < (intmins * 60):
        if (time.ticks_ms() - itertime) >= 1000:
            initvalue = not initvalue
            witty.set_boolean_value(strled, initvalue)
            itertime = time.ticks_ms()
    witty.clear_leds()

while True:
    if not witty.read_button():
        toggle_led(25, "red_led")
        toggle_led(5, "green_led")
    else:
        pass

