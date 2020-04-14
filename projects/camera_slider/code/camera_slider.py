"""This project uses the module uln2003 that you can find
at https://github.com/yeyeto2788/MicroPythonScripts/blob/master/modules/uln2003/release/uln2003.py
"""
import time
from machine import Pin
from uln2003 import Stepper, FULL_ROTATION, HALF_STEP

start_switch = Pin(4, Pin.IN, Pin.PULL_UP)
end_switch = Pin(5, Pin.IN, Pin.PULL_UP)

SLOW = 5500
FAST = 4000
FORWARD = 1
BACKWARD = -1
motor = Stepper(HALF_STEP, 15, 13, 12, 14, delay=FAST)


def fast_move(fn):
    original = motor.delay

    def wrapper(*args, **kwargs):
        motor.delay = FAST
        value = fn(*args, **kwargs)
        return value

    motor.delay = original
    return wrapper


def slow_move(fn):
    original = motor.delay

    def wrapper(*args, **kwargs):
        motor.delay = SLOW
        value = fn(*args, **kwargs)
        return value

    motor.delay = original
    return wrapper


@fast_move
def home_motor():
    """Home the motor to its starting position.

    The motor will start spindle until the end switch is activated.
    """
    while start_switch.value():
        motor.step(1, BACKWARD)

    motor.step(10)
    motor.current_position = 0


@fast_move
def get_slider_size():
    """Get the number of steps to get to the end of the slider.

    It will first home the motor and start recording the steps to get
    to the end of the slider and then home the motor again.
    """
    home_motor()

    while end_switch.value():
        motor.step(1)

    slider_length = motor.current_position
    home_motor()
    return slider_length


def timed_steps(steps, secs, count, callback=None):
    """Move the motor given steps, wait given seconds for an n given times.

    Args:
        steps: Steps to be done by the motor.
        secs: Seconds to wait until next turn.
        count: Number of time to do the repetition.
        callback: Function to be executed on each iteration.
    """

    for iteration in range(count):
        motor.step(steps)

        if callback is not None:
            callback()

        if iteration == (count - 1):
            break

        time.sleep(secs)


def go_to(destination):
    """Move the motor to a desired step number.

    The movement will be perform based on the current position of
    the motor.
    """
    current_pos = motor.current_position

    if current_pos > destination:
        movement = current_pos - destination
        direction = BACKWARD
    else:
        movement = destination - current_pos
        direction = FORWARD
    motor.step(movement, direction)


def move_to(start, end):
    """Perform a movement from point A to point B.

    First go to point A and then perform the movement to point
    B.
    """
    go_to(start)

    if start < end:
        direction = FORWARD
        x1 = start
        x2 = end
    else:
        direction = BACKWARD
        x1 = end
        x2 = start
    motor.step(x2 - x1, direction)
