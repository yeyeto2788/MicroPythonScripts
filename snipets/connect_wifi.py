import network

ssid_ = '<#your_ssid#>'
wp2_pass = '<#your_wpa2_pass#>'

sta_if = []


def do_connect():
    global sta_if
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid_, wp2_pass)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


# connecting to WiFi
do_connect()
