# MicroPomodoro
This is a script that is used to implement the Pomodoro Technique, with a 25 mins working time and 5 mins break.

This uses the OLED LCD display on the board to show the remaining time, once the time finishes the alarm will go off.

What we need to do is download all the code from the Relase folder and rename the **`Pomodoro.py`** file to **`main.py`** so it will be executed after booting up.


## Parts needed:

  * ESP8266

  I'm using the Wemos D1 Mini board.

  <p align="center">
  <img src="./Doc/images/wemos_d1_mini.png" alt="Wemos d1 mini board"  width="150"/>
  </p>

  * OLED display (I2C)

  <p align="center">
  <img src="./Doc/images/wemos_mini_oled.png" alt="Wemos D1 Oled Display"  width="150"/>
  </p>

  * Buzzer

  * LEDs or Neopixel strip.

  <p align="center">
  <img src="./Doc/images/12_neopixel_ring.png" alt="12 neopixel ring pcb"  width="150"/>
  </p>


## Usefull links:

[Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique)

## TO DO:

- [ ] Add real execution image.

- [ ] Better documentation.

- [ ] Add buzzer ring alaram when finish.

- [x] Add led or neopixel (Optional).

- [x] Add button execution.
