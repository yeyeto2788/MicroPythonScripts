import socket
import os

file_name = "messages.txt"

def check_file():
    if file_name in os.listdir():
        return True
    else:
        with open(file_name, 'w') as f:
            f.close()
        return True


def get_file_size():
    with open(file_name, 'r') as f:
        lines = f.readlines()
        f.close()
        return len(lines)


def write_file(strMessage):
    if (strMessage != '#') or (len(strMessage) > 2):
        if "+" in strMessage:
            strMessage = strMessage.replace("+", " ")
        total_messages = read_file()
        if get_file_size() > 15:
            del total_messages[0]
        total_messages.append(strMessage)
        with open(file_name, 'w') as f:
            for item in total_messages:
                f.write(item + "\n")
            f.close()


def read_file():
    filedata = []
    if check_file() is True:
        with open(file_name, "r") as messages:
            Data = messages.readlines()
            if len(Data) > 0:
                for line in Data:
                    message = line.rstrip()
                    filedata.append(message)
            else:
                filedata.append('NO MESSAGES')
    return filedata


def linted_data():
    data = []
    for element in read_file():
        data.append('<tr>\n<td>%s</td>\n</tr>' % element)
    return data


def main():
    check_file()
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
            gotten_msg = b"GET /?messageinput="
            if gotten_msg in h:
                msg = h.decode('utf-8').split('/?messageinput=')
                final_msg = msg[1][:(len(msg) - 12)]
                write_file(final_msg)
            if h == b"" or h == b"\r\n":
                break
        rows = linted_data()
        response = html % '\n'.join(rows)
        cl.send(response)
        cl.close()

main()
