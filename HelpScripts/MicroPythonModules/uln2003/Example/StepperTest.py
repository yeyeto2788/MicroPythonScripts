import uln2003, time


def hundred_steps():
    s1 = uln2003.Stepper(uln2003.HALF_STEP, 16, 15, 14, 13, delay=5000)
    print("Motor will move 100 steps clockwise")
    s1.step(100)     # Rotate 100 steps clockwise
    print("Motor will move 100 steps counter-clockwise")
    s1.step(100, -1) # Rotate 100 steps anti-clockwise


def one_by_one():
    s1 = uln2003.Stepper(uln2003.HALF_STEP, 16, 15, 14, 13, delay=5000)
    s2 = uln2003.Stepper(uln2003.HALF_STEP, 6, 5, 4, 3, delay=5000)
    print("Motor 1 will do a full rotation")
    s1.step(uln2003.FULL_ROTATION)
    print("Motor 2 will do a full rotation")
    s2.step(uln2003.FULL_ROTATION)


def both_simultaneously():
    s1 = uln2003.Stepper(uln2003.HALF_STEP, 16, 15, 14, 13, delay=5000)
    s2 = uln2003.Stepper(uln2003.HALF_STEP, 6, 5, 4, 3, delay=5000)

    print("Creating command 1")
    c1 = uln2003.Command(s1, uln2003.FULL_ROTATION)         # Go all the way round
    print("Creating command 2")
    c2 = uln2003.Command(s2, uln2003.FULL_ROTATION/2, -1)   # Go halfway round, backwards

    print("Initialize the driver class")
    runner = uln2003.Driver()
    print("Let's put both motors to run at the 'same' time")
    runner.run([c1, c2])


print("Starting hundred_steps() function.")
hundred_steps()
print("Funtion hundred_steps() finished!")
time.sleep(2)
print("Starting one_by_one() function. It will move 2 motors one by one")
one_by_one()
print("Funtion one_by_one() stopped.")
time.sleep(2)
print("Starting both_simultaneously() function. It will move both motors at the 'same' time")
both_simultaneously()
print("Funtion both_simultaneously() stopped.")
time.sleep(2)
print("Script finished!. SEE YA!")
