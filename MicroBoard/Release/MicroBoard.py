import socket
import os
import gc

file_name = "messages.txt"

def check_file():
    if file_name in os.listdir():
        return True
    else:
        with open(file_name, "w") as f:
            f.close()
        return True

def get_file_size():
    with open(file_name, "r") as f:
        lines = f.readlines()
        f.close()
        return len(lines)

def quick_decode(strdecode):
    elements = {"ñ": "%C3%B1", "€": "%E2,%AC", ";": "%3B", "?": "%3F", "/": "%2F", ":": "%3A", "#": "%23", "&": "%26",
                "=": "%3D", "+": "%2B", "$": "%24", ",": "%2C", "%": "%25", "<": "%3C", ">": "%3E", "@": "%40",
                "(": "%28", ")": "%29", "‚": "%82", "!": "%21"}
    if "+" in strdecode:
        strdecode = strdecode.replace("+", " ")
    if "%20" in strdecode:
        strdecode = strdecode.replace("%20", " ")
    for element in elements:
        if elements[element] in strdecode:
            strdecode = strdecode.replace(elements[element], element)
    return strdecode

def write_file(strMessage):
    if (strMessage != "#") or (len(strMessage) > 2):
        strMessage = quick_decode(strMessage)
        total_messages = read_file()
        if get_file_size() > 15:
            del total_messages[0]
        total_messages.append(strMessage)
        with open(file_name, "w") as f:
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
                filedata.append("NO MESSAGES")
    return filedata

def linted_data():
    data = []
    for element in read_file():
        data.append("<tr>\n<td>%s</td>\n</tr>" % element)
    return data


def main():
    check_file()
    html ="""<!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Message board</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body              { font-family: "Arial"; background: #fff;}
        .h1_div			  { background-color: #424242; height: 90px; text-align: center; font-family: "Arial";}
        .current_time     { vertical-align:middle; font-family:"Arial";}
        h1                { border-bottom: 1px; }
        h3                { font-family: "Arial"; color: #424242; text-align: center;}
        table             { table-layout: center;	font-family: "Arial";}
        th                { font-style: bold; text-align: center; height: 15px; border-bottom: 1px solid #ddd; padding: 5px}
        td                { border-bottom: 1px solid #ddd; text-align: left}
        input[type=text]  { border: 1px solid #424242; margin: 4px 2px; width:20em;}
        input[type=text]:focus { border: 3px solid #424242; margin: 4px 2px; -webkit-transition: width 0.4s ease-in-out; transition: width 0.4s ease-in-out;}
        input[type=submit]{ background-color: #424242; border: 3px; color: #ffffff; padding: 4px 8px; text-decoration: none; margin: 4px 2px; cursor: pointer; width:20em; font-weight: bold; font-family: "Arial";}
        form              {text-align: center;}
        </style>
        </head>
        <body>
        <div>
        <div class="h1_div">
        <h1 align="center" style="color:#ffffff;">Message board</h1>
        <h3 align="center" style="color:#ffffff;" class="current_time" id="humanTime"></h3>
        </div><div>
        <table align="center"><tr><th><h1>Messages</h1></th></tr>%s</table>
        <form>
        <br><h3>Type a message:</h3><br>
        <div><input type="text" name="messageinput"></input></div>
        <div><input type="submit" value="Send"></input></div>
        </form></div></div>
        <script>
        function currentTime(){var e=new Date;datestring=e.toDateString()+" "+e.toTimeString(),document.getElementById("humanTime").innerHTML=datestring.split(" ").slice(0,5).join(" ")}var element=document.getElementById("humanTime");void 0!==element&&null!=element&&(window.load=setInterval(currentTime,1e3));
        </script>
        </body>
        </html>
        """

    addr = socket.getaddrinfo("192.168.4.1", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    connection_count = 0

    while True:
        cl, addr = s.accept()
        print(connection_count, "connection on", addr)
        print("Free in: %d" % gc.mem_free())
        connection_count += 1
        cl_file = cl.makefile("rwb", 0)
        while True:
            h = cl_file.readline()
            gotten_msg = b"GET /?messageinput="
            if gotten_msg in h:
                msg = h.decode("utf-8").split("/?messageinput=")
                final_msg = msg[1][:(len(msg)-12)]
                write_file(final_msg)
            if h == b"" or h == b"\r\n":
                break
        rows = linted_data()
        response = html % "\n".join(rows)
        try:
            cl.sendall(response)
        except OSError as error:
            pass
        cl.close()
        print("Free out: %d" % gc.mem_free())


main()
