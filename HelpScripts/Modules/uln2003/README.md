# uln2003 class

This class is made for using Stepper motor 28BYJ-48

Stepper motor specs:
* Step Angle = 5.625° / 64
* Number of phase = 4
* Speed Variation Ratio = 1/64

From this data we can conclude that the **Steps per revolution** is equal to `(360 / Step Angle) / (FULL_STEP or HALF_STEP)`, there is also [this blog](http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html) that states that these motors are not that accurate so it will be needed to change the Steps per revolution for in between `508` and `509` that is why in the code the FULL_ROTATION is set to `int(4075.7728395061727 / 8)`.

The blog says the following:
>I tried to speed things up to 500pps (2ms delay between steps), but then the motor also failed the test. The maximum speed without any load was 800 pps (1.2 ms delay or 5.0 seconds for one revolution). At higher pulses, the motor just stopped.

