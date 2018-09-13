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

    def clear(self, bln_fill=0, bln_show=0):
        self.display.fill(bln_fill)
        if bln_show:
            self.display.show()

    def wrapped_text(self, pstr_message):
        word_lines = []
        if type(pstr_message) == str:
            words = pstr_message.split(" ")
            message = ""
            for iteration, word in enumerate(words):
                remaining_chars = self.max_char - len(message)
                if (len(message + " " + word) <= remaining_chars) or ((len(word) + 1) <= remaining_chars):
                    if iteration == len(words) - 1:
                        message += word + " "
                        word_lines.append(message)
                        break
                    else:
                        message += word + " "
                else:
                    if iteration == len(words) - 1:
                        word_lines.append(message)
                        message = word + (" " * remaining_chars)
                        word_lines.append(message)
                        break
                    else:
                        word_lines.append(message)
                        message = word + " "
                if len(message) >= self.max_char:
                    word_lines.append(message)
                    message = ""
        else:
            word_lines = ["Convert type ", "%s" % type(pstr_message), "to string."]
        return word_lines

    def print_wrapped(self, str_message):
        self.clear(0, 1)
        word_list = self.wrapped_text(str_message)
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

    def print_on_line(self, pstr_message, pint_line, pint_start=0):
        possible_chars = (self.width - pint_start) - self.char_width
        if len(pstr_message) > possible_chars:
            pstr_message = pstr_message[0:possible_chars]
        if pint_line < len(self.v_lines):
            self.display.text(pstr_message, pint_start, self.v_lines[pint_line])
        self.display.show()

    def draw_line(self, pint_x0, pint_y0, pint_x1, pint_y1):
        steep = abs(pint_y1 - pint_y0) > abs(pint_x1 - pint_x0)
        if steep:
            pint_x0, pint_y0 = pint_y0, pint_x0
            pint_x1, pint_y1 = pint_y1, pint_x1
        if pint_x0 > pint_x1:
            pint_x0, pint_x1 = pint_x1, pint_x0
            pint_y0, pint_y1 = pint_y1, pint_y0
        dx = pint_x1 - pint_x0
        dy = abs(pint_y1 - pint_y0)
        err = dx // 2
        if pint_y0 < pint_y1:
            ystep = 1
        else:
            ystep = -1
        while pint_x0 <= pint_x1:
            if steep:
                self.display.pixel(pint_y0, pint_x0, 1)
            else:
                self.display.pixel(pint_x0, pint_y0, 1)
            err -= dy
            if err < 0:
                pint_y0 += ystep
                err += dx

            pint_x0 += 1
        self.display.show()

    def draw_hline(self, pint_x, pint_y, width, pbln_show=1):
        if pint_y < 0 or pint_y > self.height or pint_x < -width or pint_x > self.width:
            return
        for iteration in range(width):
            self.display.pixel(pint_x + iteration, pint_y, 1)
        if pbln_show:
            self.display.show()

    def draw_vline(self, pint_x, pint_y, height, pbln_show=1):
        if pint_y < -height or pint_y > self.height or pint_x < 0 or pint_x > self.width:
            return
        for iteration in range(height):
            self.display.pixel(pint_x, pint_y + iteration, 1)
        if pbln_show:
            self.display.show()

    def draw_circle(self, pint_x, pint_y, radius):
        f = 1 - radius
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius
        self.display.pixel(pint_x, pint_y + radius, 1)
        self.display.pixel(pint_x, pint_y - radius, 1)
        self.display.pixel(pint_x + radius, pint_y, 1)
        self.display.pixel(pint_x - radius, pint_y, 1)
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
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
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self.draw_vline(pint_x + x, pint_y - y, 2 * y + 1, 0)
            self.draw_vline(pint_x + y, pint_y - x, 2 * x + 1, 0)
            self.draw_vline(pint_x - x, pint_y - y, 2 * y + 1, 0)
            self.draw_vline(pint_x - y, pint_y - x, 2 * x + 1, 0)
        self.display.show()

    def draw_rect(self, pint_x0, pint_y0, width, height):
        if pint_y0 < -height or pint_y0 > self.height or pint_x0 < -width or pint_x0 > self.width:
            return
        self.draw_hline(pint_x0, pint_y0, width, 0)
        self.draw_hline(pint_x0, pint_y0 + height - 1, width, 0)
        self.draw_vline(pint_x0, pint_y0, height, 0)
        self.draw_vline(pint_x0 + width - 1, pint_y0, height, 0)
        self.display.show()

    def draw_rect_filled(self, pint_x0, pint_y0, width, height):
        if pint_y0 < -height or pint_y0 > self.height or pint_x0 < -width or pint_x0 > self.width:
            return
        for iteration in range(pint_x0, pint_x0 + width):
            self.draw_vline(iteration, pint_y0, height, 0)
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

    def set_brightness(self, pint_contrast):

        if pint_contrast <= 255:
            self.display.contrast(pint_contrast)

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
