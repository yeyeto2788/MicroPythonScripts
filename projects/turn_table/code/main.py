import gc
import time
import socket

from uln2003 import Stepper, FULL_ROTATION, HALF_STEP

DIRECTION = 1
SLOW = 5500
FAST = 4000
STATES = {
    0: "Idle",
    1: "Working"
}
STATE = STATES[0]
ANGLE_STRING = b"angle="
DELAY_STRING = b"delay="
COUNT_STRING = b"count="

motor = Stepper(HALF_STEP, 15, 13, 12, 14, delay=FAST)


def move_n_degrees(degrees, delay=0, count=1):
    """Perform a rotation on the motor n degrees n times.

    Also set the current state to `working` when performing the operations.

    Args:
        degrees: degrees to rotate.
        delay: time between each rotation.
        count: number of repetitions

    Returns:
        None.
    """
    global STATE
    STATE = STATES[1]
    start = 1 if count > 1 else 0

    for index in range(start, count):
        motor.rel_angle(degrees)
        time.sleep(delay)
    STATE = STATES[0]


def main():
    global STATE
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)

    html = """<!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Micro Turntable</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body              { font-family: "Arial"; background: #fff; margin:0;; color: #000}
        a                 {color: #fff;}
        a:visited         {color: #fff;}
        .h1_div			  { background-color: #424242; height: 90px; text-align: center;}
        .current_time     { vertical-align:middle;}
        h1                { border-bottom: 1px; }
        h3                { color: #424242; text-align: center;}
        table             { table-layout: center;}
        th                { font-style: bold; text-align: center; height: 20px; border-bottom: 1px solid #ddd}
        td                { border-bottom: 1px solid #ddd; text-align: left}
        input[type=text]  { border: 1px solid #424242; width:10em;}
        input[type=text]:focus { border: 3px solid #424242; margin: 4px 2px; -webkit-transition: width 0.4s ease-in-out; transition: width 0.4s ease-in-out;}
        input[type=submit]{ background-color: #424242; border: 3px; color: #ffffff; padding: 4px; text-decoration: none; margin: auto; cursor: pointer; width:30em; font-weight: bold;}
        form              {text-align: center;}
        </style>
        </head>
        <body>
        <div>
        <div class="h1_div">
        <h1 align="center" style="color:#ffffff;"><a href="http://192.168.4.1">Micro Turntable</a></h1>
        </div><div>
        <form>
        <br><h2>Parameters:</h2><br>
        <table align="center">
        <tr><th><h3>Degrees</h3></th><th><h3>Delay</h3></th><th><h3>Count</h3></th></tr>
        <tr><th><input type="text" name="angle" /></th><th><input type="text" name="delay" /></th><th><input type="text" name="count" /></th></tr>
        <tr><th colspan="3"><input type="submit" value="Send" /></th></tr>
        </table>
        </form></div><br><br><br><br>
        <div align="center"><h2>Status:</h2><p>%s</p></div></div>
        </body>
        </html>
        """

    connection_count = 0
    angle = 0
    delay = 0
    count = 0

    while True:
        cl, addr = s.accept()
        print(connection_count, "connection on", addr)
        print("Free in: %d" % gc.mem_free())
        connection_count += 1
        cl_file = cl.makefile("rwb", 0)
        while True:
            h = cl_file.readline()
            print(h)
            # Parse headers to get the values.
            if ANGLE_STRING in h:
                try:
                    angle = int(h.split(ANGLE_STRING)[1].split(b'&')[0])
                    STATE = STATES[1]
                except ValueError:
                    angle = 0
            if DELAY_STRING in h:
                try:
                    delay = int(h.split(DELAY_STRING)[1].split(b"&")[0])
                except ValueError:
                    delay = 0
            if COUNT_STRING in h:
                try:
                    count = int(h.split(COUNT_STRING)[1].split(b" ")[0])
                except ValueError:
                    count = 0
            # Last header sent
            if h == b"" or h == b"\r\n":
                break

        response = html % "\n".join(STATE)

        try:
            cl.sendall(response)
        except OSError as error:
            print("Error trying to send all information. %s" % error)
            pass

        cl.close()
        print("Free out: %d" % gc.mem_free())
        print("Got angle=%s, delay=%s and count=%s" % (
            str(angle), str(delay), str(count)
        )
              )
        if angle > 0:
            move_n_degrees(angle, delay, count)
        #  Reset the values.
        angle = 0
        delay = 0
        count = 0
