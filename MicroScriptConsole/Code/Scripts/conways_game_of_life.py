from time import sleep_ms
from console import Button
from console import Display
from urandom import getrandbits

"""
This code was ported from the https://github.com/mcauser/MicroPython-ESP8266-Nokia-5110-Conways-Game-of-Life
so most of the credit goes to Mike Causer
"""


class ConwaysGameOfLife:
    def __init__(self):
        self.best = 0
        self.oled = Display()
        self.width = self.oled.width
        self.height = self.oled.height
        self.select_button = Button(0)

    def center_text(self, txt):
        """
        This function will center all incomming strings to a fix size of the display
        max_char property.

        Args:
            txt: String to be centered.

        Returns:
            type: String with the text centered
        """
        return '{: ^{}}'.format(txt, self.oled.max_char)

    def intro(self):
        """
        It will print the intro on the oled display with a sleep of 1 second so
        the message will be visible.

        Returns:
            Nothing.
        """
        self.oled.display.fill(0)
        self.oled.print_on_line(self.center_text("Conway's"), 2)
        self.oled.print_on_line(self.center_text("Game"), 3)
        self.oled.print_on_line(self.center_text("of"), 4)
        self.oled.print_on_line(self.center_text("Life"), 5)
        sleep_ms(1000)

    def end(self, generations, best, size):
        """
        It will ouput on the oled display the Generations, best score and the
        size of the pixels.

        Args:
            generations: Integer with the generations created.
            best: Integer the best score.
            size: Integer with the size of the pixels.

        Returns:
            Nothing.
        """
        self.oled.clear(0, 1)
        self.oled.print_on_line(self.center_text("Generations"), 0)
        self.oled.print_on_line(self.center_text(str(generations)), 1)
        self.oled.print_on_line(self.center_text("Best Score"), 3)
        self.oled.print_on_line(self.center_text(str(best)), 4)
        self.oled.print_on_line(self.center_text("Pixel Size"), 5)
        self.oled.print_on_line(self.center_text(str(size)), 6)
        sleep_ms(2000)
        self.oled.clear(0, 1)

    def begin(self, size=4, delay=20):
        """
        Main function to check the button to stop the game or if game has ended.
        If so, then call the `end` function to show the results.

        Args:
            size: Integer with the size of the pixels.
            delay: Integer of the delay between generations (In milliseconds).

        Returns:
            Nothing.
        """
        self.size = size # Size of lifeforms in pixels
        self.delay = delay # Delay in ms between generations

        # Localised to avoid self lookups
        # Possible performance optimisation, TBC
        delay = self.delay
        tick = self.tick
        self.randomise() # Randomise initial pixels

        generations = 0 # Begin
        try:
            while (tick() and self.select_button.is_released()):
                generations = generations + 1
                self.oled.display.show()
                sleep_ms(delay)
        except KeyboardInterrupt:
            pass

        if generations > self.best: # New high score?
            self.best = generations

        self.end(generations, self.best, self.size) # End

    def randomise(self):
        """
        Generate a seudo-random cells on the screen.

        Returns:
            Nothing.
        """
        size = self.size
        width = self.width
        height = self.height
        self.oled.display.fill(0)

        for x in range(0, width, size):
            for y in range(0, height, size):
                # random bit: 0 = pixel off, 1 = pixel on
                self.cell(x, y, getrandbits(1))

    def cell(self, x, y, colour):
        """
        This will assign a value to a given pixel.

        Args:
            x: Integer with the `x` axis position.
            y: Integer with the `y` axis position.
            colour: Boolean with the value to be assigned.

        Returns:
            Nothing.
        """
        size = self.size
        for i in range(size):
            for j in range(size):
                self.oled.display.pixel(x + i, y + j, colour)

    def get(self, x, y):
        """
        Function to return the value of the given pixel x, y.

        Args:
            x: Integer with the `x` axis position.
            y: Integer with the `y` axis position.

        Returns:
            type: Boolean with the value of the pixel.
        """
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return 0
        if self.oled.display.pixel(x, y) is None:
            bln_return = getrandbits(1)
        else:
            bln_return = self.oled.display.pixel(x, y)
        return bln_return & 1

    def tick(self):
        """
        This function will apply the game rules getting the live cells and the ones
        that have to die.

        Returns:
            Boolean to keep the game going or not.
        """
        size = self.size
        width = self.width
        height = self.height
        get = self.get
        cell = self.cell

        # If no pixels are born or die, the game ends
        something_happened = False

        for x in range(0, width, size):
            for y in range(0, height, size):

                alive = get(x, y) # Is the current cell alive

                # Count number of neighbours
                neighbours = (
                    get(x - size, y - size) +
                    get(x, y - size) +
                    get(x + size, y - size) +
                    get(x - size, y) +
                    get(x + size, y) +
                    get(x + size, y + size) +
                    get(x, y + size) +
                    get(x - size, y + size)
                )

                # Apply the game rules
                if alive and not 2 <= neighbours <= 3:
                    cell(x, y, 0) # This pixel dies
                    if not something_happened:
                        something_happened = True
                elif not alive and neighbours == 3:
                    cell(x, y, 1) # A new pixel is born
                    if not something_happened:
                        something_happened = True
        return something_happened


a = ConwaysGameOfLife()
a.intro()
a.begin(4, 10)
