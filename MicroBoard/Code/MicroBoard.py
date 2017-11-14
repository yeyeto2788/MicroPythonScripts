import socket

html = b"""<!DOCTYPE html>
<html lang="en">
<head>
  <title>Message board</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="style.css">
</head>
<body>
<h1>Message board</h1>
<table><tr><th>Messages</th><th>Time</th></tr>%s</table>
<form>
    <br><h3>Type a message:</h3><br>
    <input type="text" name="messageinput"></input>
    <input type="submit" value="Send"></input>
</form>
</body>
</html>
"""

def ReadFile():
    tabledata= []
    with open("messages.txt", "r") as messages:
        for line in messages.readlines():
            message = line.split(",")
            tabledata.append("<tr>\n<td>%s</td>\n<td>%s</td>\n</tr>" % (message[0], message[1]))
    return tabledata
    
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
    rows = ReadFile()
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
