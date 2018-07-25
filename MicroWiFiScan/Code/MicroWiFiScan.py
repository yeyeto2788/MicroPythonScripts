import network
import machine
import ssd1306
import utime
import gc
gc.enable()


class DisplayWifi:
    def __init__(self, sda_pin=5, scl_pin=4):
        """
        Initialize the function with the pins 5,4 (sda, scl respectively) by default.

        In this function we initialize the i2c bus and the screen and activate WiFi radio.

        Args:
            sda_pin: integer with the pin number assigned for SDA
            scl_pin: integer with the pin number assigned for SCL
        """
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
        """
        Try to do a WiFi available connections and than format the text that will be display on the
        screen.

        If WiFi scan fails the display will show NONE on the entire segments of the screen.

        Returns:
            Nothing.
        """
        try:
            wlan_list = self.wlan.scan()
        except:
            wlan_list = [['NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE']]
        for intCounter in wlan_list:
            self.name = str(intCounter[0], 'utf8')
            self.strength = str(intCounter[3]) + ' dBm'
            self.kanaal = 'Channel: ' + str(intCounter[2])
            self.status = self.get_secure(intCounter[4])
            self.show_display()
            self.oled.fill(0)
            self.oled.show()

    @staticmethod
    def get_secure(num):
        """
        Convert the number returned by the Wifi scan to a test showing what type of
        Wifi security it is.

        If the number is not recognized it will just return the number as a string.

        Args:
            num: integer with the type of security.

        Returns:
            strReturn: String with the description of the Wifi security.
        """
        strReturn = ""
        try:
            if int(num) == 0:
                strReturn = 'Open wifi'
            elif int(num) == 1:
                strReturn = 'WEP'
            elif int(num) ==2:
                strReturn = 'WPA-PSK'
            elif int(num) == 3:
                strReturn = 'WPA2-PSK'
            elif int(num) == 4:
                strReturn = 'WPA/WPA2-PSK'
            else:
                strReturn = str(num)

            return strReturn
        except:
            return strReturn

    def show_display(self):
        """
        Cleans the screen  and show all data.

        If network names are longer than the display's width it will split the name in two
        and show it will be shown on row 1,2.

        Returns:
            Nothing.
        """

        self.oled.fill(0)
        self.oled.show()
        if len(self.name) > 15:
            self.oled.text(self.name[0:15],0,0)
            self.oled.text(self.name[15:int(len(self.name))],0,8)
        else:
            self.oled.text(self.name,0,0)
            self.oled.text(self.strength, 30, 20)
            self.oled.text(self.status,30,30)
            self.oled.text(self.kanaal, 30,40)
            self.oled.text((str(gc.mem_free())+ " B"), 30,50)
            self.oled.show()
            utime.sleep_ms(10000)

    def __str__(self):
        return "Name: {}.\n{}\n{}.\n{}.".format(self.name, self.strength, self.kanaal, self.status)
