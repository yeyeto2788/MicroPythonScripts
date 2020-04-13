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
motor = Stepper(HALF_STEP, 15, 13, 12, 14, delay=FAST)


def home_motor():
    """Home the motor to its starting position.

    The motor will start spindle until the end switch is activated.
    """
    while start_switch.value():
        motor.step(1, -1)

    motor.step(10)
    motor.current_position = 0


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
