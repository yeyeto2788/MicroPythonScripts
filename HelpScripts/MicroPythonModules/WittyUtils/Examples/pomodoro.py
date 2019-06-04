from wittyUtils import WittyBoard
import time

witty = WittyBoard()


def toggle_led(intmins, strled):
    """
    Toggles an LED for a given amount of minutes.

    Args:
        intmins: Integer with the minutes to toggle the led.
        strled: String with the name of the led.

    Returns:
        Nothing.
    """
    initvalue = 0
    initial_time = time.ticks_ms()
    itertime = initial_time
    witty.clear_leds()
    while ((time.ticks_ms() - initial_time) / 1000) < (intmins * 60):
        if (time.ticks_ms() - itertime) >= 1000:
            initvalue = not initvalue
            witty.set_boolean_value(strled, initvalue)
            itertime = time.ticks_ms()
    witty.clear_leds()


witty.clear_leds()
while True:
    if not witty.read_button():
        witty.set_boolean_value('blue_led', 0)
        toggle_led(25, "red_led")
        toggle_led(5, "green_led")
    else:
        witty.set_boolean_value('blue_led', 1)
