import network
import machine
import ssd1306
import utime
import gc
gc.enable()


class WiFiScanner:
    def __init__(self, sda_pin=5, scl_pin=4):
        
        self.sda_pin = sda_pin
        self.scl_pin = scl_pin
        self.name = ''
        self.strength = ''
        self.status = ''
        self.kanaal = ''
        self.i2c = machine.I2C(scl=machine.Pin(self.scl_pin), sda=machine.Pin(self.sda_pin))
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        self.oled.fill(1)
        self.oled.show()
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def format(self):
        
        try:
            wlan_list = self.wlan.scan()
        except:
            wlan_list = [['NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE']]
        for counter in wlan_list:
            self.name = str(counter[0], 'utf8')
            self.strength = str(counter[3]) + ' dBm'
            self.kanaal = 'Channel: ' + str(counter[2])
            self.status = self.get_secure(counter[4])
            self.show_display()
            self.oled.fill(0)
            self.oled.show()

    @staticmethod
    def get_secure(num):
        
        s_return = ""
        try:
            if int(num) == 0:
                s_return = 'Open wifi'
            elif int(num) == 1:
                s_return = 'WEP'
            elif int(num) ==2:
                s_return = 'WPA-PSK'
            elif int(num) == 3:
                s_return = 'WPA2-PSK'
            elif int(num) == 4:
                s_return = 'WPA/WPA2-PSK'
            else:
                s_return = str(num)

            return s_return
        except:
            return s_return

    def show_display(self):
        

        self.oled.fill(0)
        self.oled.show()
        if len(self.name) > 15:
            self.oled.text(self.name[0:15], 0, 0)
            self.oled.text(self.name[15:int(len(self.name))], 0, 8)
        else:
            self.oled.text(self.name, 0, 0)
            self.oled.text(self.strength, 30, 20)
            self.oled.text(self.status, 30, 30)
            self.oled.text(self.kanaal, 30, 40)
            self.oled.text((str(gc.mem_free()) + " B"), 30, 50)
            self.oled.show()
            utime.sleep_ms(10000)

    def __str__(self):
        return "Name: {}.\n{}\n{}.\n{}.".format(self.name, self.strength, self.kanaal, self.status)
