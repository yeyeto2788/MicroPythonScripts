"""You need to be connected to internet in order to execute the request"""
import machine
import ntptime

ntptime.host = "es.pool.ntp.org"

try:
    ntptime.settime()
except OSError:
    print('ERROR: Cannot set time via ntp')

rtc = machine.RTC()
print(rtc.datetime())
