import time
from console import Display

oled = Display()


oled.print_wrapped("Scanning I2C Devices on the bus...")
time.sleep(0.5)
devices = oled.i2c.scan()

if len(devices) == 0:
    oled.clear(0, 1)
    oled.print_wrapped("No I2C devices found :(")

else:
    oled.clear(0, 1)
    oled.print_wrapped('%s I2C devices found' % str(len(devices)))
    time.sleep(1.5)

    for count in range(1, 2):
        for device in devices:
            oled.clear(0, 1)
            oled.print_on_line("Decimal address:", 2)
            oled.print_on_line(str(device), 3)
            oled.print_on_line("Hex address:", 4)
            oled.print_on_line(str(hex(device)), 5)
            time.sleep(1)
        oled.clear(0, 1)
