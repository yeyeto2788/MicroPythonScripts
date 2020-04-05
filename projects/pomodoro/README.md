# MicroPomodoro
This is a script that is used to implement the Pomodoro Technique, with a 25 mins working time and 5 mins break.

This uses the OLED LCD display on the board to show the remaining time, once the time finishes the alarm will go off.

What we need to do is download all the code from the **`Release`** folder and rename the **`pomodoro.py`** file to **`main.py`** so it will be executed after booting up.


## Parts needed:

  * ESP8266

  I'm using the Wemos D1 Mini board.

  <p align="center">
  <img src="../../static/images/wemos_d1_mini.png" alt="Wemos d1 mini board"  width="200"/>
  </p>

  * OLED display (I2C)

  <p align="center">
  <img src="../../static/images/wemos_mini_oled.png" alt="Wemos D1 Oled Display"  width="200"/>
  </p>

  * Buzzer

  * LEDs or Neopixel strip.

  <p align="center">
  <img src="../../static/images/12_neopixel_ring.png" alt="12 neopixel ring pcb"  width="200"/>
  </p>

## Custom PCB for the project.
<p align="center">
<table align="center">
  <tr>
    <th>Version</th>
    <th>Top side of the board</th>
    <th>Placement of components</th>
    <th colspan="2">Comments</th>
  </tr>
  <tr>
    <td>Version 0.1</td>
    <td><img src="docs/images/v01_pomodoro_pcb_top.png" alt="Top side of board"  width="300"/></td>
    <td><img src="docs/images/v01_pomodoro_pcb_top_placement.png" alt="Placement of components"  width="300"/></td>
    <td colspan="2">Use this version if you do not wish to use the OLED LCD display.</td>
  </tr>
  <tr>
    <td>Version 0.2</td>
    <td><img src="docs/images/v02_pomodoro_pcb_top.png" alt="Top side of board"  width="300"/></td>
    <td><img src="docs/images/v02_pomodoro_pcb_bottom.png" alt="Placement of components"  width="300"/></td>
    <td colspan="2">This version comes with 4 push buttons and 2 I2C connectors. You can see  <a href="docs/pdf/Schematics_v02.pdf">schematics</a> here.</td>
  </tr>
</table>
</p>

The idea with this board it not to have wires all over and also makes it better for fitting it into a 3D printed case (If anyone can help me out would be great) and also for connecting it to the Wemos D1 mini board.

 ~~I'll try to keep the design for single side PCB.~~ Since the price of making the PCBs is not that expensive, I decided to make it double sided to add more things on the board.

Eagle CAD files are within the **`Release`** folder

#### Bill of materials
<table align="center">
  <tr>
    <th>Item</th>
    <th>Quantity</th>
  </tr>
  <tr>
    <td>WS2812B Neopixel</td>
    <td>12</td>
  </tr>
  <tr>
    <td>100 pf Capacitor (SMD 1206)</td>
    <td>12</td>
  </tr>
  <tr>
    <td>SMD 1k Resistor (SMD 1206)</td>
    <td>4</td>
  </tr>
  <tr>
    <td>6mm Push button</td>
    <td>4</td>
  </tr>
  <tr>
    <td>Plain PCB (around 6x6 cm)</td>
    <td>1</td>
  </tr>
</table>


**The PCB is still in testing stage.** (Currently testing Version 0.2)


## Useful links:

[Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique)

## TO DO:

- [ ] Add real execution image.

- [ ] Better documentation.

- [ ] Add buzzer ring alarm when finish.

- [ ] Add Eagle CAD design file, Gerber files and PDF for manual PCB manufacturing.
  <ul><li> - [x] Eagle Files</li>
  <li> - [ ] Gerber files.</li>
  <li> - [X] PDF files.</li></ul>

- [x] Add led or neopixel (Optional).

- [x] Add button execution.
