# MicroProblemSolver
This is a script that is used to implement the Rubber duck debugging Technique asking questions so by this it will be forcing themselves (programmers) to explain it, line-by-line, to the duck.

This uses the OLED LCD display on the board to show the question being asked so the problem can be somehow solved, this questions are taken randomly from the `questions.json` file in the repository that needs to be uploaded into the board.

What we need to do is download all the code from the **`Release`** folder so it will be executed after booting up.

So in the board you'll have the following files:
* `main.py` (Renamed `problem_solver.py` file without comments.)
* `questions.json` (File with questions that can be change or even add more.)

Once all files are in the board, every time you want a random question you just need to reset the board.

## Parts needed:

  * **ESP8266**

  I'm using the Wemos D1 Mini board.

  <p align="center">
  <img src="./Doc/images/wemos_d1_mini.png" alt="Wemos d1 mini board"  width="200"/>
  </p>

  * **OLED display (I2C)**

  <p align="center">
  <img src="./Doc/images/wemos_mini_oled.png" alt="Wemos D1 Oled Display"  width="200"/>
  </p>


## Useful links:

[Rubber duck debugging](https://en.wikipedia.org/wiki/Rubber_duck_debugging)


## TO DO:

- [ ] Add real execution image.

- [ ] Better documentation.
