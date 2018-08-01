import time, machine

FULL_ROTATION = int(4075.7728395061727 / 8)

HALF_STEP = [
[0, 0, 0, 1],
[0, 0, 1, 1],
[0, 0, 1, 0],
[0, 1, 1, 0],
[0, 1, 0, 0],
[1, 1, 0, 0],
[1, 0, 0, 0],
[1, 0, 0, 1],
]

FULL_STEP = [
[1, 0, 1, 0],
[0, 1, 1, 0],
[0, 1, 0, 1],
[1, 0, 0, 1]
]

class Command():
    def __init__(self, stepper, steps, direction=1):
        self.stepper = stepper
        self.steps = steps
        self.direction = direction

class Driver():

    @staticmethod
    def run(commands):
        max_steps = sum([c.steps for c in commands])
        count = 0
        while count != max_steps:
            for command in commands:
                # we want to interleave the commands
                if command.steps > 0:
                    command.stepper.step(1, command.direction)
                    command.steps -= 1
                    count += 1

class Stepper():
    def __init__(self, mode, pin1, pin2, pin3, pin4, delay=2000):
        self.mode = mode
        self.pin1 = machine.Pin(pin1, machine.Pin.OUT)
        self.pin2 = machine.Pin(pin2, machine.Pin.OUT)
        self.pin3 = machine.Pin(pin3, machine.Pin.OUT)
        self.pin4 = machine.Pin(pin4, machine.Pin.OUT)
        self.delay = delay  # Recommend 10000+ for FULL_STEP, 1000 is OK for HALF_STEP
        self.steps_per_rev = FULL_ROTATION
        self.current_position = 0
        self.reset()  # Initialize all to 0

    def step(self, step_count, direction=1):
        for x in range(step_count):
            for bit in self.mode[::direction]:
                self.pin1.value(bit[0])
                self.pin2.value(bit[1])
                self.pin3.value(bit[2])
                self.pin4.value(bit[3])
                time.sleep_us(self.delay)
        self.current_position += (direction * step_count)

    def rel_angle(self, angle):
        steps = int(angle / 360 * self.steps_per_rev)
        self.step(steps)

    def abs_angle(self, angle):
        steps = int(angle / 360 * self.steps_per_rev)
        steps -= self.current_position % self.steps_per_rev
        self.step(steps)

    def revolution(self, rev_count):
        self.step(rev_count * self.steps_per_rev)

    def set_step_delay(self, us):
        if us < 20:  # 20 us is the shortest possible for esp8266
            self.delay = 20
        else:
            self.delay = us

    def set_steps_per_revolution(self):
        self.steps_per_rev = int((360 / (5.625 / 64)) / len(self.mode))

    def reset(self):
        self.pin1.value(0)
        self.pin2.value(0)
        self.pin3.value(0)
        self.pin4.value(0)
        if self.current_position > 0:
            self.current_position = 0
