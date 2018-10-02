"""
IMPORT MODULES NEEDED
"""
import socket
import dht
import gc
import machine


"""
DECLARE FUNCTIONS
"""

def ReadSensors():
    """
    Read the DHT11 sensor for Temperature and

    Returns:
            An array with the temperature and the humidity read from the sensor.
    """
    data = []
    d = dht.DHT11(machine.Pin(2))
    d.measure()
    Temperature = d.temperature()
    Humidity = d.humidity()
    for i in range(0,1):
        data.append('<tr><td align="center"><h3>%s C</h3></td><td align="center"><h3>%s &#37;</h3></td></tr>' % (str(Temperature), str(Humidity)))
    return data


def main():
    """
    Main code to be executed, all logic it is within this function.

    Returns:
            None
    """
    html = b"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Weather Station</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <META HTTP-EQUIV="refresh" CONTENT="30">
    <style>
    body              { font-family: 'Arial'; background: #fff; }
    .h1_div			  { background-color: #80deea; height: 90px;  line-height: 90px;  text-align: center; font-family: 'Arial';}
    h1                { border-bottom: 1px; }
    h3                { font-family: 'Arial'; text-align: center;}
    table             { table-layout: center;	font-family: 'Arial';}
    th                { font-style: bold; text-align: center; height: 15px; border-bottom: 1px solid #ddd; padding: 5px; color:#424242;}
    td                { border-bottom: 1px solid #ddd; text-align: left; color:#424242;}
    </style>
    </head>
    <body>
    <div>
    <div class="h1_div">
    	<h1 align='center' style="color:#424242;">ESP8266 Weather Station</h1><br>
    </div>
    <div>
    <table align="center"><tr><th><h2>Temperature</h2></th><th><h2>Humidity</h2></th></tr>%s</table>
    </div>
    <div><p align="center"><b>NOTE:</b> This page will automatically refresh every 30 seconds.</p></div>
    </div>
    </body>
    </html>
    """
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        print("Free in: %d" % gc.mem_free())
        cl_file = cl.makefile('rwb', 0)
        while True:
            h = cl_file.readline()
            if h == b"" or h == b"\r\n":
                break
        rows = ReadSensors()
        response = html % '\n'.join(rows)
        try:
            cl.sendall(response)
        except OSError as error:
            print("Error trying to send all information. %s" % error)
            pass
        cl.close()


"""
EXECUTE THE CODE
"""
main()
