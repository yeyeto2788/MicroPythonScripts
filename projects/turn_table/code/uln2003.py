import time
import machine

LOW = 0
HIGH = 1
FULL_ROTATION = int(4075.7728395061727 / 8)

HALF_STEP = [
    [LOW, LOW, LOW, HIGH],
    [LOW, LOW, HIGH, HIGH],
    [LOW, LOW, HIGH, LOW],
    [LOW, HIGH, HIGH, LOW],
    [LOW, HIGH, LOW, LOW],
    [HIGH, HIGH, LOW, LOW],
    [HIGH, LOW, LOW, LOW],
    [HIGH, LOW, LOW, HIGH],
]

FULL_STEP = [
    [HIGH, LOW, HIGH, LOW],
    [LOW, HIGH, HIGH, LOW],
    [LOW, HIGH, LOW, HIGH],
    [HIGH, LOW, LOW, HIGH]
]


class Command:
    """
    Tell a stepper to move X many steps in a given direction
    """
    def __init__(self, stepper, steps, direction=1):
        self.stepper = stepper
        self.steps = steps
        self.direction = direction


class Driver:
    """
    Drive a set of motors, each with their own commands
    """

    @staticmethod
    def run(commands):
        """
        Takes commands and calls the step function from the Stepper class in other to seem they are moving at the same time.

        Args:
            commands: List with the commands to execute.

        Returns:
            Nothing.
        """

        # Work out total steps to take
        max_steps = sum([c.steps for c in commands])

        count = 0
        while count != max_steps:
            for command in commands:
                # we want to interleave the commands
                if command.steps > 0:
                    command.stepper.step(1, command.direction)
                    command.steps -= 1
                    count += 1


class Stepper:
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
        """
        Rotates the Stepper motor a given number of steps. It also sets the current position of the stepper.

        Args:
            step_count: integer with the number of steps to do.
            direction: integer (1 or -1) for forward and backward direction.

        Returns:
            Nothing.
        """
        for x in range(step_count):
            for bit in self.mode[::direction]:
                self.pin1.value(bit[0])
                self.pin2.value(bit[1])
                self.pin3.value(bit[2])
                self.pin4.value(bit[3])
                time.sleep_us(self.delay)
        self.current_position += (direction * step_count)

    def rel_angle(self, angle):
        """
        Rotate stepper for given relative angle.

        Args:
            angle: Integer with the angle.

        Returns:
            Nothing.
        """
        steps = int(angle / 360 * self.steps_per_rev)
        self.step(steps)

    def abs_angle(self, angle):
        """
        Rotate stepper for given absolute angle since last power on.

        Args:
            angle: Integer with the angle.

        Returns:
            Nothing.
        """
        steps = int(angle / 360 * self.steps_per_rev)
        steps -= self.current_position % self.steps_per_rev
        self.step(steps)

    def revolution(self, rev_count):
        """
        Perform given number of full revolutions.

        Args:
            rev_count: Integer with the number of revolution to do.

        Returns:
            Nothing.
        """
        self.step(rev_count * self.steps_per_rev)

    def set_step_delay(self, us):
        """
        Set time in microseconds between each step.

        Args:
            us: integer with the number of microseconds.

        Returns:
            Nothing.
        """
        if us < 20:  # 20 us is the shortest possible for esp8266
            self.delay = 20
        else:
            self.delay = us

    def set_steps_per_revolution(self):
        """
        Calculate the number of steps needed for one revolution.

        Returns:
            Nothing.
        """
        self.steps_per_rev = int((360 / (5.625 / 64)) / len(self.mode))

    def reset(self):
        """
        Power off the motors and reset the steps count to zero.

        Returns:
            Nothing.
        """
        self.pin1.value(0)
        self.pin2.value(0)
        self.pin3.value(0)
        self.pin4.value(0)
        if self.current_position > 0:
            self.current_position = 0
