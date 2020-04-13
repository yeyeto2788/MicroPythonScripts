import time
from machine import Pin
from uln2003 import Stepper,FULL_ROTATION,HALF_STEP
start_switch=Pin(4,Pin.IN,Pin.PULL_UP)
end_switch=Pin(5,Pin.IN,Pin.PULL_UP)
SLOW=5500
FAST=4000
motor=Stepper(HALF_STEP,15,13,12,14,delay=FAST)
def home_motor():
 while start_switch.value():
  motor.step(1,-1)
 motor.step(10)
 motor.current_position=0
def timed_steps(steps,secs,count,callback=None):
 for iteration in range(count):
  motor.step(steps)
  if callback is not None:
   callback()
  if iteration==(count-1):
   break
  time.sleep(secs)
