import time
from machine import Pin
from uln2003 import Stepper,FULL_ROTATION,HALF_STEP
start_switch=Pin(4,Pin.IN,Pin.PULL_UP)
end_switch=Pin(5,Pin.IN,Pin.PULL_UP)
SLOW=5500
FAST=4000
FORWARD=1
BACKWARD=-1
motor=Stepper(HALF_STEP,15,13,12,14,delay=FAST)
def fast_move(fn):
 original=motor.delay
 def wrapper(*args,**kwargs):
  motor.delay=FAST
  value=fn(*args,**kwargs)
  return value
 motor.delay=original
 return wrapper
def slow_move(fn):
 original=motor.delay
 def wrapper(*args,**kwargs):
  motor.delay=SLOW
  value=fn(*args,**kwargs)
  return value
 motor.delay=original
 return wrapper
@fast_move
def home_motor():
 while start_switch.value():
  motor.step(1,BACKWARD)
 motor.step(10)
 motor.current_position=0
@fast_move
def get_slider_size():
 home_motor()
 while end_switch.value():
  motor.step(1)
 slider_length=motor.current_position
 home_motor()
 return slider_length
def timed_steps(steps,secs,count,callback=None):
 for iteration in range(count):
  motor.step(steps)
  if callback is not None:
   callback()
  if iteration==(count-1):
   break
  time.sleep(secs)
def go_to(destination):
 current_pos=motor.current_position
 if current_pos>destination:
  movement=current_pos-destination
  direction=BACKWARD
 else:
  movement=destination-current_pos
  direction=FORWARD
 motor.step(movement,direction)
def move_to(start,end):
 go_to(start)
 if start<end:
  direction=FORWARD
  x1=start
  x2=end
 else:
  direction=BACKWARD
  x1=end
  x2=start
 motor.step(x2-x1,direction)
