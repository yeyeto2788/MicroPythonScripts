import webrepl
import network
import displaywifi
webrepl.start()

display = displaywifi.DisplayWifi(5,4)
while True:
    display.format()
#Uncomment code below to see the output on the REPL or WebREPL
#print(display)
