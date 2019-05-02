import webrepl
import wifi_scan
webrepl.start()

display = wifi_scan.WiFiScanner(5, 4)
while True:
    display.format()

#Uncomment code below to see the output on the REPL or WebREPL
#print(display)
