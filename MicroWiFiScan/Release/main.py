import webrepl
import network
import MicroWiFiScan
webrepl.start()

display = MicroWiFiScan.WiFiScanner(5,4)
while True:
    display.format()
#Uncomment code below to see the output on the REPL or WebREPL
#print(display)
