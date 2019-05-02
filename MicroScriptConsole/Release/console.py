import machine
import ssd1306
import time

class Display(object):
    def __init__(self, width=128, height=64):
        self.i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
        self.width = width
        self.height = height
        self.char_width = 8
        self.max_char = int(self.width / self.char_width)
        self.v_lines = [i * self.char_width for i in range(int(self.height / self.char_width))]
        self.display = ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)
        self.clear(0, 1)

    def clear(self, fill=0, show=0):
        self.display.fill(fill)
        if show:
            self.display.show()

    def wrapped_text(self, message):
        word_lines = []
        if type(message) == str:
            words = message.split(" ")
            msg = ""
            for iteration, word in enumerate(words):
                remaining_chars = self.max_char - len(msg)
                if (len(msg + " " + word) <= remaining_chars) or ((len(word) + 1) <= remaining_chars):
                    if iteration == len(words) - 1:
                        msg += word + " "
                        word_lines.append(msg)
                        break
                    else:
                        msg += word + " "
                else:
                    if iteration == len(words) - 1:
                        word_lines.append(msg)
                        msg = word + (" " * remaining_chars)
                        word_lines.append(msg)
                        break
                    else:
                        word_lines.append(msg)
                        msg = word + " "
                if len(msg) >= self.max_char:
                    word_lines.append(msg)
                    msg = ""
        else:
            word_lines = ["Convert type ", "%s" % type(message), "to string."]
        return word_lines

    def print_wrapped(self, message):
        self.clear(0, 1)
        word_list = self.wrapped_text(message)
        line_counter = 0
        for iteration in range(len(word_list)):
            if line_counter >= len(self.v_lines):
                time.sleep(3)
                line_counter = 0
            if line_counter == 0:
                self.clear(0, 1)
            self.display.text(word_list[iteration], 0, self.v_lines[line_counter])
            self.display.show()
            line_counter += 1

    def print_on_line(self, message, line, start=0):
        possible_chars = (self.width - start) - self.char_width
        if len(message) > possible_chars:
            message = message[0:possible_chars]
        if line < len(self.v_lines):
            self.display.text(message, start, self.v_lines[line])
        self.display.show()

    def draw_line(self, x0, y0, x1, y1):
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx // 2
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1
        while x0 <= x1:
            if steep:
                self.display.pixel(y0, x0, 1)
            else:
                self.display.pixel(x0, y0, 1)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx

            x0 += 1
        self.display.show()

    def pixel(self, x, y, color):
        super(self.display, self).pixel(x, y, color)

    def draw_hline(self, x, y, width, show=1):
        if y < 0 or y > self.height or x < -width or x > self.width:
            return
        for iteration in range(width):
            self.display.pixel(x + iteration, y, 1)
        if show:
            self.display.show()

    def draw_vline(self, x, y, height, show=1):
        if y < -height or y > self.height or x < 0 or x > self.width:
            return
        for iteration in range(height):
            self.display.pixel(x, y + iteration, 1)
        if show:
            self.display.show()

    def draw_circle(self, pint_x, pint_y, radius):
        f = 1 - radius
        dd_f_x = 1
        dd_f_y = -2 * radius
        x = 0
        y = radius
        self.display.pixel(pint_x, pint_y + radius, 1)
        self.display.pixel(pint_x, pint_y - radius, 1)
        self.display.pixel(pint_x + radius, pint_y, 1)
        self.display.pixel(pint_x - radius, pint_y, 1)
        while x < y:
            if f >= 0:
                y -= 1
                dd_f_y += 2
                f += dd_f_y
            x += 1
            dd_f_x += 2
            f += dd_f_x
            self.display.pixel(pint_x + x, pint_y + y, 1)
            self.display.pixel(pint_x - x, pint_y + y, 1)
            self.display.pixel(pint_x + x, pint_y - y, 1)
            self.display.pixel(pint_x - x, pint_y - y, 1)
            self.display.pixel(pint_x + y, pint_y + x, 1)
            self.display.pixel(pint_x - y, pint_y + x, 1)
            self.display.pixel(pint_x + y, pint_y - x, 1)
            self.display.pixel(pint_x - y, pint_y - x, 1)
        self.display.show()

    def draw_circle_filled(self, pint_x, pint_y, radius):
        self.draw_vline(pint_x, pint_y - radius, 2 * radius + 1, 0)
        f = 1 - radius
        dd_f_x = 1
        dd_f_y = -2 * radius
        x = 0
        y = radius
        while x < y:
            if f >= 0:
                y -= 1
                dd_f_y += 2
                f += dd_f_y
            x += 1
            dd_f_x += 2
            f += dd_f_x
            self.draw_vline(pint_x + x, pint_y - y, 2 * y + 1, 0)
            self.draw_vline(pint_x + y, pint_y - x, 2 * x + 1, 0)
            self.draw_vline(pint_x - x, pint_y - y, 2 * y + 1, 0)
            self.draw_vline(pint_x - y, pint_y - x, 2 * x + 1, 0)
        self.display.show()

    def draw_rect(self, x, y, width, height):
        if y < -height or y > self.height or x < -width or x > self.width:
            return
        self.draw_hline(x, y, width, 0)
        self.draw_hline(x, y + height - 1, width, 0)
        self.draw_vline(x, y, height, 0)
        self.draw_vline(x + width - 1, y, height, 0)
        self.display.show()

    def draw_rect_filled(self, x, y, width, height):
        if y < -height or y > self.height or x < -width or x > self.width:
            return
        for iteration in range(x, x + width):
            self.draw_vline(iteration, y, height, 0)
        self.display.show()

    @staticmethod
    def hex2bits(hexstr):
        bitstr = ""
        for pos in range(0, len(hexstr) - 1, 2):
            newhex = hexstr[pos:pos + 2]
            newint = int(newhex, 16)
            newbin = bin(newint)[2:]
            newbits = '0' * (8 - len(newbin)) + newbin
            bitstr += newbits
        return bitstr

    def draw_graphic(self, file, pint_x=0, pint_y=0):
        image_file = open(file, "r")
        pic = image_file.readlines()
        for y, row in enumerate(pic):
            line = self.hex2bits(row.rstrip('\r\n'))
            for x, col in enumerate(line):
                if col == "1":
                    self.display.pixel(pint_x + x, pint_y + y, 1)
                else:
                    self.display.pixel(pint_x + x, pint_y + y, 0)
        self.display.show()

    def set_brightness(self, contrast):
        if contrast <= 255:
            self.display.contrast(contrast)

class Button(object):

    def __init__(self, pin):
        self._pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)

    def read(self):
        return not self._pin.value()

    def isPressed(self):
        return self.read()

    def isReleased(self):
        return not self.read()

class Keypad(object):

    def __init__(self, up=14, down=13, select=12, start=0):
        self.UP = machine.Pin(up, machine.Pin.IN, machine.Pin.PULL_UP)
        self.DOWN = machine.Pin(down, machine.Pin.IN, machine.Pin.PULL_UP)
        self.SELECT = machine.Pin(select, machine.Pin.IN, machine.Pin.PULL_UP)
        self.START = machine.Pin(start, machine.Pin.IN, machine.Pin.PULL_UP)

    def get_key_value(self, pkey):
        return pkey.value()

    def get_keypad(self):
        keys = [self.UP, self.DOWN, self.SELECT, self.START]
        values = []
        for key in keys:
            values.append(self.get_key_value(key))
        return values

class ConsoleError(Exception):
    pass
