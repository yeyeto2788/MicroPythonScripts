from time import sleep_ms
from console import Button
from console import Display
from urandom import getrandbits

class ConwaysGameOfLife:
    def __init__(self):
        self.best = 0
        self.oled = Display()
        self.width = self.oled.width
        self.height = self.oled.height
        self.select_button = Button(0)

    def center_text(self, txt):
        return '{: ^{}}'.format(txt, self.oled.max_char)

    def intro(self):
        self.oled.display.fill(0)
        self.oled.print_on_line(self.center_text("Conway's"), 2)
        self.oled.print_on_line(self.center_text("Game"), 3)
        self.oled.print_on_line(self.center_text("of"), 4)
        self.oled.print_on_line(self.center_text("Life"), 5)
        sleep_ms(1000)

    def end(self, generations, best, size):
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
        self.size = size
        self.delay = delay 
        delay = self.delay
        tick = self.tick
        self.randomise() 
        generations = 0
        try:
            while (tick() and self.select_button.isReleased()):
                generations = generations + 1
                self.oled.display.show()
                sleep_ms(delay)
        except KeyboardInterrupt:
            pass

        if generations > self.best: 
            self.best = generations

        self.end(generations, self.best, self.size) 

    def randomise(self):
        size = self.size
        width = self.width
        height = self.height
        self.oled.display.fill(0)

        for x in range(0, width, size):
            for y in range(0, height, size):
                self.cell(x, y, getrandbits(1))

    def cell(self, x, y, colour):
        size = self.size
        for i in range(size):
            for j in range(size):
                self.oled.display.pixel(x + i, y + j, colour)

    def get(self, x, y):
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return 0
        if self.oled.display.pixel(x, y) is None:
            bln_return = getrandbits(1)
        else:
            bln_return = self.oled.display.pixel(x, y)
        return bln_return & 1

    def tick(self):
        size = self.size
        width = self.width
        height = self.height
        get = self.get
        cell = self.cell
        something_happened = False

        for x in range(0, width, size):
            for y in range(0, height, size):
                alive = get(x, y)
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

                if alive and not 2 <= neighbours <= 3:
                    cell(x, y, 0) 
                    if not something_happened:
                        something_happened = True
                elif not alive and neighbours == 3:
                    cell(x, y, 1) 
                    if not something_happened:
                        something_happened = True
        return something_happened

a = ConwaysGameOfLife()
a.intro()
a.begin(4, 10)
