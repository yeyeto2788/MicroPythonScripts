# uln2003 class

This class is made for using Stepper motor 28BYJ-48

Stepper motor specs:
* Step Angle = 5.625° / 64
* Number of phase = 4
* Speed Variation Ratio = 1/64

From this data we can conclude that the **Steps per revolution** is equal to `(360 / (5.625° / 64)) / (FULL_STEP or HALF_STEP)`, there is also [this blog](http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html) that states that these motors are not that accurate so it will be needed to change the Steps per revolution for in between `508` and `509` that is why in the code the FULL_ROTATION is set to `int(4075.7728395061727 / 8)`.

The blog says the following:
>I tried to speed things up to 500pps (2ms delay between steps), but then the motor also failed the test. The maximum speed without any load was 800 pps (1.2 ms delay or 5.0 seconds for one revolution). At higher pulses, the motor just stopped.

Also keep in mind that a delay of less than 5 microseconds may cause the motor to simply buzz and not move at all.


**Usage:**

To use the module in a easy way we can do something like:

```python
import uln2003
s1 = uln2003.Stepper(uln2003.HALF_STEP, 16, 15, 14, 13, delay=50)
s1.step(100)     # Rotate 100 steps clockwise
s1.step(100, -1) # Rotate 100 steps anti-clockwise
s1.step(uln2003.FULL_ROTATION) # Rotate 360 degrees clockwise
s1.step(uln2003.FULL_ROTATION, -1) # Rotate 360 degrees anti-clockwise
```

The code above will be using `HALF_STEP` variable to do a half-stepping that it will take **8** steps to rotate the motor (Not taking into account the gears on the motor) if we want to do full-stepping we have to use the `FULL_STEP` variable that it will take **4** steps to rotate the motor (Also not taking into account the gears on the motor.

We can instantiate more that one motor on the same script, to do so we can do something like:

```python
import uln2003
s1 = uln2003.Stepper(uln2003.HALF_STEP, 16, 15, 14, 13, delay=5000)
s2 = uln2003.Stepper(uln2003.HALF_STEP, 6, 5, 4, 3, delay=5000)
s1.step(uln2003.FULL_ROTATION)# Rotate 360 degrees clockwise
s2.step(uln2003.FULL_ROTATION)# Rotate 360 degrees clockwise
```

This code will make a full rotation of the motor (Taking into account the gears on it), first the motor 1 (`s1`) and then (`s2`).

If we want to move two motor at the "same" time we can do the following:

```python
import uln2003
s1 = uln2003.Stepper(uln2003.HALF_STEP, 16, 15, 14, 13, delay=5000)
s2 = uln2003.Stepper(uln2003.HALF_STEP, 6, 5, 4, 3, delay=5000)
c1 = uln2003.Command(s1, uln2003.FULL_ROTATION)         # Go all the way round
c2 = uln2003.Command(s2, uln2003.FULL_ROTATION/2, -1)   # Go halfway round, backwards
runner = uln2003.Driver()
runner.run([c1, c2])
```
---
## Useful Variables:

Within the module we have some useful variable that will help us to track the motor position or even the steps per revolution used on the motor.

* **Stepper.delay**: Delay between steps (Recommend 10000+ for `FULL_STEP`, 1000 is OK for `HALF_STEP`)
* **Stepper.steps_per_rev**: By default it set to `FULL_ROTATION` which has a value of (`int(4075.7728395061727 / 8)` about 509)
* **Stepper.current_position**: It will give you the current count of steps done by the motor.

---
## Functions:

* ### **Stepper.step(step_count, direction)**
  Rotates the Stepper motor a given number of steps.

  It also sets the current position of the stepper.

  The direction is set to 1 by default (clockwise)

  ##### **Arguments**
   * **`step_count`**: Integer with the number of steps to do.
   * **`direction`**: Integer (1 or -1) for forward and backward direction.

* ### **Stepper.rel_angle(angle)**
  Rotate stepper for given relative angle.

  ##### **Arguments**
  * **`angle`**: Integer with the angle degrees.

* ### **Stepper.abs_angle(angle)**
  Rotate stepper for given absolute angle since last power on.

  ##### **Arguments**
  * **`angle`**: Integer with the angle degrees.

* ### **Stepper.revolution(rev_count)**
  Perform given number of full revolutions (360 degrees taking into account the motor gears)

  ##### **Arguments**
  * **`rev_count`**: Integer with the number of revolution to do.

* ### **Stepper.set_step_delay(us)**
  Set time in microseconds between each step.

  Take into account that 20 us is the shortest possible for esp8266

  ##### **Arguments**
  * **`us`**: Integer with the number of microseconds.

* ### **Stepper.set_steps_per_revolution()**
  Calculate and set the number of steps needed for one revolution.


* ### **Stepper.reset()**
  Power off the motors and reset the steps count to zero.

---
