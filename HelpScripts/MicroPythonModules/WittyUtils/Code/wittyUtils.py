import machine


class WittyBoard:
    IN = 0
    OUT = 1
    PWM = 2
    pins = {"leds": {
                        "green_led": {
                            "pin": 12,
                            "mode": OUT
                        },
                        "red_led": {
                            "pin": 15,
                            "mode": OUT
                        },
                        "blue_led": {
                            "pin": 13,
                            "mode": OUT
                        },
                        "builtin_led": {
                            "pin": 2,
                            "mode": OUT
                        }
                    },
            "button": {
                        "pin": 4,
                        "mode": IN
                      }
        }

    @classmethod
    def clear_leds(cls):
        """
        Turns off the leds on the board.

        Returns:
            Nothing.
        """
        for pin in cls.pins['leds']:
            if pin != 'builtin_led':
                if cls.pins['leds'][pin]['mode'] == cls.PWM:
                    machine.PWM(machine.Pin(cls.pins['leds'][pin]['pin'])).deinit()
                cls.pins['leds'][pin]['mode'] = cls.OUT
                machine.Pin(cls.pins['leds'][pin]['pin'], machine.Pin.OUT).off()

    @classmethod
    def read_button(cls):
        """
        Reads the actual value of the button on the board

        Returns:
            Button input value.
        """
        return machine.Pin(cls.pins['button']['pin'], machine.Pin.IN).value()

    @staticmethod
    def read_adc():
        """
        Reads the value from the Analog to Digital converter.

        Returns:
            The actual value of the ADC.
        """
        return machine.ADC(0).read()

    @classmethod
    def set_boolean_value(cls, strled, blnstatus):
        """
        Turns off and on the given led.
        
        Args:
            strled: String with the name of the led
            blnstatus: Boolean to which you want to set the led to.

        Returns:
            Nothing.
        """
        if strled in cls.pins['leds']:
            if cls.pins['leds'][strled]['mode'] == cls.PWM:
                machine.PWM(machine.Pin(cls.pins['leds'][strled]['pin'])).deinit()
                cls.pins['leds'][strled]['mode'] = cls.OUT
            machine.Pin(cls.pins['leds'][strled]['pin'], machine.Pin.OUT).value(blnstatus)


    @classmethod
    def set_pwm_value(cls, strled, intduty):
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
        if strled in cls.pins['leds']:
            machine.PWM(machine.Pin(cls.pins['leds'][strled]['pin']), freq=500).duty(intduty)
            cls.pins['leds'][strled]['mode'] = cls.PWM
