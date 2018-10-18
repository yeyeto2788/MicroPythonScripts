import time
import machine
from console import Display

oled = Display()
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

oled.clear(0, 1)
oled.print_wrapped('Scanning devices on the I2C bus...')
devices = i2c.scan()
time.sleep(0.5)

if len(devices) == 0:
    oled.clear(0, 1)
    oled.print_wrapped("No I2C devices found :(")
else:
    oled.clear(0, 1)
    oled.print_wrapped('%s I2C devices found' % str(len(devices)))
    time.sleep(1.5)

    for intloop in range(1,2):
        for device in devices:
            oled.clear(0, 1)
            oled.print_on_line("Decimal address:")
            oled.print_on_line(str(device))
            oled.print_on_line("Hex address:")
            oled.print_on_line(str(hex(device)))
            time.sleep(1)
