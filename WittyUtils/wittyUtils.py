import machine


class WittyBoard:

    pins = {"leds": {"green_led": 12, "red_led": 15, "blue_led": 13, "builtin_led": 2}, "button": 4}

    @classmethod
    def clear_leds(cls):
        """
        Turns off the leds on the board.

        Returns:
            Nothing.
        """

        for pin in cls.pins['leds'].values():
            if pin != cls.pins['leds']['builtin_led']:
                machine.PWM(machine.Pin(pin)).deinit()
                machine.Pin(pin, machine.Pin.OUT).off()

    @classmethod
    def read_button(cls):
        """
        Reads the actual value of the button on the board

        Returns:
            Button input value.
        """
        return machine.Pin(cls.pins['button'], machine.Pin.IN).value()

    @staticmethod
    def read_adc():
        """
        Reads the value from the Analog to Digital converter.

        Returns:
            The actual value of the ADC.
        """
        return machine.ADC(0).read()

    @classmethod
    def set_led_value(cls, strled, intduty):
        """
        Will set a PWM pin for setting brightness off the led. There are some parameter to take into account which are
        written below.
                duty: 0 - 1023 (pin being high)
                freq: 1Hz - 1Khz
        Args:
            strled: String with the name of the led
            intduty: Integer for the duty on the PWM

        Returns:
            Nothing.
        """
        if strled in cls.pins['leds'].keys():
            machine.PWM(machine.Pin(cls.pins['leds'][strled]), freq=500).duty(intduty)
