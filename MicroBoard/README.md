# MicroBoard

The idea of this script is to host a bulleting board on a webserver based on the ESP8266 where it will read the messages stored on a file called `messages.txt` from within the ESP8266 . This will create an access point to where you can connect and read the messages and post messages on it.

What we need to do is download all the code from the `Relase` folder and rename the `MicroBoard.py` file to `main.py` so it will be executed after booting up.

If you want to clean the `messages.txt` just go ahead and also put the `boot.py` script on the board and it will check if there are more than 10 messages and if so clean the file.

### Image of how it should look like:
![Server testing running image](https://github.com/yeyeto2788/MicroPythonScripts/blob/master/MicroBoard/Doc/index.png)


## TO DO:

- [ ] Add real execution image.

- [ ] Better documentation.
