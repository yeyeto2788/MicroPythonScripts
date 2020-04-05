import picoweb
import network

app = picoweb.WebApp("app")

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp, content_type="text/html")

    html_file = open('index.html', 'r')

    for line in html_file:
        yield from resp.awrite(line)

def get_ip():
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

host_ip = get_ip()
app.run(debug=True, host=host_ip)
