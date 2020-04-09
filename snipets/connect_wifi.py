import time
import network

ssid_ = '<#your_ssid#>'
wp2_pass = '<#your_wpa2_pass#>'


def do_connect(retries=5):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid_, wp2_pass)
        while not sta_if.isconnected() and retries <= 5:
            print("Executing code in '{}' seconds.".format(retries))
            if retries < 0:
                break
            else:
                time.sleep(1)
            retries -= 1
            pass
    print('network config:', sta_if.ifconfig())


# connecting to WiFi
do_connect()
