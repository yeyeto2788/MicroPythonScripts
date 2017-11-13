import network
import socket

html = b"""<!DOCTYPE html>
<html>
<head>
  <title>Message board</title>
</head>
<body>

<h1>Message board</h1>
<table align="center">
  <tr>
    <th>Messages</th>
    <th>Time</th>
  </tr>
  %s
</table>
 <form align="center" method="post">
    <br><h3>Type a message:</h3><br>
    <input type="text" name="messageinput">
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
    

s = socket.socket()    
addr = socket.getaddrinfo('192.168.4.1', 8080)[0][-1]
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
    rows = ["<tr>\n<td>hola</td>\n<td>hola</td>\n</tr>", "<tr>\n<td>hola</td>\n<td>pepito</td>\n</tr>"] #ReadFile()
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
