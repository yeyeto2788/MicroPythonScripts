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
        for pin in cls.pins['leds']:
            if pin != 'builtin_led':
                if cls.pins['leds'][pin]['mode'] == cls.PWM:
                    machine.PWM(machine.Pin(cls.pins['leds'][pin]['pin'])).deinit()
                cls.pins['leds'][pin]['mode'] = cls.OUT
                machine.Pin(cls.pins['leds'][pin]['pin'], machine.Pin.OUT).off()

    @classmethod
    def read_button(cls):
        return machine.Pin(cls.pins['button']['pin'], machine.Pin.IN).value()

    @staticmethod
    def read_adc():
        return machine.ADC(0).read()

    @classmethod
    def set_boolean_value(cls, strled, blnstatus):
        if strled in cls.pins['leds']:
            if cls.pins['leds'][strled]['mode'] == cls.PWM:
                machine.PWM(machine.Pin(cls.pins['leds'][strled]['pin'])).deinit()
                cls.pins['leds'][strled]['mode'] = cls.OUT
            machine.Pin(cls.pins['leds'][strled]['pin'], machine.Pin.OUT).value(blnstatus)


    @classmethod
    def set_pwm_value(cls, strled, intduty):
        if strled in cls.pins['leds']:
            machine.PWM(machine.Pin(cls.pins['leds'][strled]['pin']), freq=500).duty(intduty)
            cls.pins['leds'][strled]['mode'] = cls.PWM
