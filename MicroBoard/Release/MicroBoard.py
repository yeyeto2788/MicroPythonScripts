import socket
import os

def CheckFile():
    Files = os.listdir()
    File = "messages.txt"
    if File in Files:
        return True
    else:
        with open(File, 'w') as f:
            f.close()
        return True

def WriteFile(msgString):
    with open('messages.txt', 'ab') as f:
        f.write(msgString + "\n")
        f.close()

def ReadFile():
    tabledata = []
    if CheckFile() is True:
        with open("messages.txt", "r") as messages:
            Data = messages.readlines()
            if len(Data) > 0:
                for line in Data:
                    message = line.rstrip()
                    tabledata.append('<tr>\n<td>%s</td>\n</tr>' % message)
            else:
                tabledata.append('<tr><td>NO MESSAGES</td>\n</tr>')
    return tabledata


def main():
    html = """<!DOCTYPE html>
    <html lang="en">
    <head>
      <title>Message board</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    <h1>Message board</h1>
    <table><tr><th>Messages</th></tr>%s</table>
    <form>
        <br><h3>Type a message:</h3><br>
        <input type="text" name="messageinput"></input>
        <input type="submit" value="Send"></input>
    </form>
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
            GetMsg = b"GET /?messageinput="
            if GetMsg in h:
                msg = h.decode('utf-8').split('/?messageinput=')
                Final_msg = msg[1][:(len(msg)-12)]
                WriteFile(Final_msg)
            if h == b"" or h == b"\r\n":
                break
        rows = ReadFile()
        response = html % '\n'.join(rows)
        cl.send(response)
        cl.close()

main()
