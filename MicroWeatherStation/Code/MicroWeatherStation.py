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
            An array with the temperature and the humidity.
    """
    d = dht.DHT11(machine.Pin(4))
    Temperature = str(d.temperature())
    Humidity = str(d.humidity())
    data = "<tr><td>%s ºC</td><td>%s %</td></tr>" % (Temperature, Humidity)
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
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
    <h1>ESP8266 Weather Station</h1>
    <table><tr><th>Temperature</th><th>Humidity</th></tr>%s</table>
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
