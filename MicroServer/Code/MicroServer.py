import picoweb
import network

app = picoweb.WebApp("app")

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp, content_type="text/html")

    htmlFile = open('index.html', 'r')

    for line in htmlFile:
      yield from resp.awrite(line)

def getIP():
    wlan = network.WLAN(network.STA_IF)
    if wlan.active():
        addr = wlan.ifconfig()[0]
    else:
        wlan = network.WLAN(network.AP_IF)
        if wlan.active():
            addr = wlan.ifconfig()[0]
        else:
            print("No active connection")
    return addr

HostIP = getIP()
app.run(debug=True, host=HostIP)
