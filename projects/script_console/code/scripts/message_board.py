import socket, os, gc, time, console

file_name = "messages.txt"


def check_file():
    """
    Check wether the file exists or not on the directory and if not create it.

    Returns:
        True
    """
    if file_name in os.listdir():
        return True
    else:
        with open(file_name, "w") as f:
            f.close()
        return True


def get_file_size():
    """
    Get the number of lines on the file which should match with the number of messages.

    Returns:
        Integer with the number of lines on the file.

    """
    with open(file_name, "r") as f:
        lines = f.readlines()
        f.close()
        return len(lines)


def quick_decode(s_decode):
    """
    Simple function to decode data coming from http request into readable format.

    Args:
        s_decode: String to be decoded.

    Returns:
        String decoded.

    """
    elements = {"ñ": "%C3%B1", "€": "%E2,%AC", ";": "%3B", "?": "%3F", "/": "%2F", ":": "%3A",
                "#": "%23", "&": "%26", "=": "%3D", "+": "%2B", "$": "%24", ",": "%2C", "%": "%25",
                "<": "%3C", ">": "%3E", "@": "%40", "(": "%28", ")": "%29", "‚": "%82", "!": "%21"}
    if "+" in s_decode:
        s_decode = s_decode.replace("+", " ")
    if "%20" in s_decode:
        s_decode = s_decode.replace("%20", " ")
    for element in elements:
        if elements[element] in s_decode:
            s_decode = s_decode.replace(elements[element], element)
    return s_decode


def write_file(message):
    """
    This will fill information on the file in the filesystem where all messages are stored.

    Args:
        message: Message to be saved.

    Returns:
        None
    """
    if (message != "#") or (len(message) > 2):
        message = quick_decode(message)
        total_messages = read_file()
        if get_file_size() > 15:
            del total_messages[0]
        total_messages.append(message)
        with open(file_name, "w") as f:
            for item in total_messages:
                f.write(item + "\n")
            f.close()


def read_file():
    """
    Read data from file in the filesystem which should have messages, in case there is no messages
    it will return the `NO MESSAGES` in a list.

    Returns:
        file_data (lst)

    """
    file_data = []
    if check_file() is True:
        with open(file_name, "r") as messages:
            data = messages.readlines()
            if len(data) > 0:
                for line in data:
                    message = line.rstrip()
                    file_data.append(message)
            else:
                file_data.append("NO MESSAGES")
    return file_data


def linted_data():
    """
    Return a string with data from the `read_file` function in a HTML format.

    Returns:
        data (str)
    """
    data = []
    for element in read_file():
        data.append("<tr>\n<td>%s</td>\n</tr>" % element)
    return data


def main():
    """
    Main logic is on this function
    """
    oled = console.Display()
    oled.print_wrapped("Checking messages file.")
    oled.clear(0, 1)
    time.sleep(1)
    check_file()
    html = """<!DOCTYPE html>
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
        function currentTime()
        {
            var date = new Date();
            datestring = date.toDateString() + " " + date.toTimeString();
            document.getElementById("humanTime").innerHTML = datestring.split(" ").slice(0, 5).join(" ");
        }
        var element = document.getElementById("humanTime");
        if (typeof(element) != "undefined" && element != null)
        {
            window.load = setInterval(currentTime, 1000);
        }
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
        oled.print_wrapped(str("Connection from : %s" % addr) + str("Free in: %d" % gc.mem_free()))
        time.sleep(0.1)
        oled.clear(0, 1)
        connection_count += 1
        cl_file = cl.makefile("rwb", 0)
        while True:
            h = cl_file.readline()
            gotten_msg = b"GET /?messageinput="
            if gotten_msg in h:
                msg = h.decode("utf-8").split("/?messageinput=")
                final_msg = msg[1][:(len(msg)-12)]
                oled.clear(0, 1)
                oled.print_wrapped(final_msg)
                write_file(final_msg)
            if h == b"" or h == b"\r\n":
                break
        rows = linted_data()
        response = html % "\n".join(rows)
        try:
            cl.sendall(response)
        except OSError as error:
            print("Error trying to send all information. %s" % error)
            pass
        cl.close()
        oled.print_wrapped(str("Free out: %d" % gc.mem_free()))
        time.sleep(0.1)
        oled.clear(0, 1)


if __name__ == "__main__":
    main()
