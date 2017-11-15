"""
IMPORT MODULES NEEDED
"""
import socket
import dht
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
        data.append( '<tr><td align="center">%s C</td><td align="center">%s </td></tr>' % (str(Temperature), str(Humidity)))
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
      <META HTTP-EQUIV="refresh" CONTENT="15">
    </head>
    <body>
    <h1 align="center">ESP8266 Weather Station</h1>
    <table align="center"><tr><th>Temperature</th><th>Humidity</th></tr>%s</table>
    </body>
    </html>
    """
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            h = cl_file.readline()
            if h == b"" or h == b"\r\n":
                break
        rows = ReadSensors()
        response = html % '\n'.join(rows)
        cl.send(response)
        cl.close()


"""
EXECUTE THE CODE
"""
main()
