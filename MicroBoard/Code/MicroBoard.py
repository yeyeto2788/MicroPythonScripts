"""
IMPORT MODULES NEEDED
"""
import socket
import os


"""
DECLARE FUNCTIONS
"""

file_name = "messages.txt"

def check_file():
    """
    Check that the file for the messages exist, if not create the file so when we read it
    we don't get an error.

    Returns:
            True after checking if the file exists or after creating it.
    """
    if file_name in os.listdir():
        return True
    else:
        with open(file_name, 'w') as f:
            f.close()
        return True

def get_file_size():
    """
    This will return the number of lines of the file.

    Returns:
        An integer with the lines on file.
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()
        f.close()
        return len(lines)

def quick_decode(strdecode):
    """
    This will perform a nasty url decode on a given string.
    Args:
        strdecode: String to be decoded.

    Returns:
        strdecode: String decoded.
    """
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
    """
    Write messages to the file 'messages.txt' coming from the input form.
    
    Args:
        strMessage: String to be stored on the file

    Returns:
            Nothing
    """
    if (strMessage != '#') or (len(strMessage) > 2):
        strMessage = quick_decode(strMessage)
        total_messages = read_file()
        if get_file_size() > 15:
            del total_messages[0]
        total_messages.append(strMessage)
        with open(file_name, 'w') as f:
            for item in total_messages:
                f.write(item + "\n")
            f.close()

def read_file():
    """
    Read the 'messages.txt' file for the messages stored in it.

    Returns:
            An array with the messages and the 'time' next to the message.
    """
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
    """
    Add the HTML tags for each line on the file return by read_file method.

    Returns:
        data: A list with the linted data.
    """
    data = []
    for element in read_file():
        data.append('<tr>\n<td>%s</td>\n</tr>' % element)
    return data


def main():
    """
    Main core of the script, all execution goes within here.
    
    Returns:
            Nothing.
    """
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
                final_msg = msg[1][:(len(msg)-12)]
                write_file(final_msg)
            if h == b"" or h == b"\r\n":
                break
        rows = linted_data()
        response = html % '\n'.join(rows)
        cl.sendall(response)
        cl.close()

"""
EXECUTE THE CODE
"""
main()
