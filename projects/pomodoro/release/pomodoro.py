import time
import json
import machine
import neopixel
import urandom
APP_STATUS=None
try:
 import ssd1306
 BLN_DISPLAY=True
except ImportError as error:
 print("Seems like there is no such module",error)
 BLN_DISPLAY=False
def load_config():
 with open("config.json","r")as conf_file:
  return json.load(conf_file)
config=load_config()
async def slow_fill_color(neostrip,colors,pstrColor,pixel_count):
 for i in range(0,pixel_count):
  neostrip[i]=colors[pstrColor]
  time.sleep_ms(25)
  neostrip.write()
def get_random_int():
 int_return=urandom.getrandbits(8)
 if int_return<256:
  return int_return
 else:
  return 0
def display_msg(message,line,start=0,show=0):
 lines=[0,8,16,24,32,40,48]
 if line in lines:
  display.text(message,start,line)
 if show:
  display.show()
def clear_display(fill=0,show=0):
 display.fill(fill)
 if show:
  display.show()
def print_text(text):
 clear_display()
 fill_amount=16
 display_msg("*"*fill_amount,24,0,1)
 display_msg("{:*^16}".format(text),32,0,1)
 display_msg("*"*fill_amount,40,0,1)
 time.sleep(1)
 clear_display(0,1)
async def lapse_time(neostrip,minutes,color,message=""):
 t_mins=minutes-1
 for mins in range(t_mins,-1,-1):
  for secs in range(60,0,-1):
   data="{:02d} : {:02d}".format(mins,secs)
   print("Remaining time:",data)
   for milisecs in range(40,0,-1):
    set_pixel_color(neostrip,milisecs%12,color)
    time.sleep_ms(25)
   if BLN_DISPLAY:
    clear_display()
    display_msg(data,24,32)
    display_msg("{:^16}".format(message),0)
    display.show()
def set_pixel_color(neostrip,neopixel,color):
 brightness=config["neopixel"]["brightness"]
 if neostrip[neopixel]!=(0,0,0):
  neostrip[neopixel]=(0,0,0)
 else:
  if color in config["colors"]:
   final_color=[]
   for sub_color in config["colors"][color]:
    new_sub_color=int(sub_color*(brightness/100))
    if new_sub_color<0:
     new_sub_color=sub_color
    final_color.append(new_sub_color)
   neostrip[neopixel]=tuple(final_color)
 neostrip.write()
def color_neostrip(neostrip,color,pixel_count):
 if color in config["colors"]:
  brightness=config["neopixel"]["brightness"]
  for intcounter in range(pixel_count):
   rgb_color=[int(sub_color*(brightness/100))for sub_color in config["colors"][color]]
   neostrip[intcounter]=rgb_color
 neostrip.write()
async def clear_neostrip(neostrip):
 neostrip.fill=config["colors"]["nocolor"]
 neostrip.write()
async def main_logic():
 global display
 global BLN_DISPLAY
 global APP_STATUS
 if BLN_DISPLAY:
  try:
   i2c=machine.I2C(scl=machine.Pin(config["screen"]["sda"]),sda=machine.Pin(config["screen"]["scl"]))
   display=ssd1306.SSD1306_I2C(config["screen"]["width"],config["screen"]["height"],i2c)
   clear_display()
  except OSError:
   print("Error trying to initialize the code for the OLED")
   BLN_DISPLAY=False
   display=None
 button_ul=machine.Pin(config["button_ul"]["pin"],machine.Pin.IN,machine.Pin.PULL_UP)
 button_ur=machine.Pin(config["button_ur"]["pin"],machine.Pin.IN,machine.Pin.PULL_UP)
 button_dl=machine.Pin(config["button_dl"]["pin"],machine.Pin.IN,machine.Pin.PULL_UP)
 button_dr=machine.Pin(config["button_dr"]["pin"],machine.Pin.IN,machine.Pin.PULL_UP)
 neostrip=neopixel.NeoPixel(machine.Pin(config["neopixel"]["pin"]),config["neopixel"]["count"])
 await clear_neostrip(neostrip)
 colors=config["colors"]
 while True:
  if button_ul.value()==0:
   print(f"Got 'button_ul' pressed. APP_STATUS={APP_STATUS}")
   time.sleep_ms(200)
   if APP_STATUS=="ul":
    print("Setting status to 'None'")
    APP_STATUS=None
    color_neostrip(neostrip,"nocolor",config["neopixel"]["count"])
   else:
    print("Setting status to 'ul'")
    APP_STATUS=="ul"
    await lapse_time(neostrip,25,"red","POMODORO")
    await lapse_time(neostrip,5,"green","FREE TIME")
  elif button_ur.value()==0:
   print(f"Got 'button_ur' pressed. APP_STATUS={APP_STATUS}")
   time.sleep_ms(150)
   if APP_STATUS=="ur":
    print("Setting status to 'None'")
    APP_STATUS=None
    color_neostrip(neostrip,"nocolor",config["neopixel"]["count"])
   else:
    print("Setting status to 'ur'")
    APP_STATUS=="ur"
    for color in colors:
     color_neostrip(neostrip,color,config["neopixel"]["count"])
     time.sleep_ms(250)
     color_neostrip(neostrip,"nocolor",config["neopixel"]["count"])
  elif button_dl.value()==0:
   print(f"Got 'button_dl' pressed. APP_STATUS={APP_STATUS}")
   time.sleep_ms(200)
   if APP_STATUS=="dl":
    print("Setting status to 'None'")
    APP_STATUS=None
    color_neostrip(neostrip,"nocolor",config["neopixel"]["count"])
   else:
    print("Setting status to 'dl'")
    APP_STATUS="dl"
    for color in colors:
     await slow_fill_color(neostrip,colors,color,config["neopixel"]["count"])
     time.sleep_ms(100)
     color_neostrip(neostrip,"nocolor",config["neopixel"]["count"])
  elif button_dr.value()==0:
   print(f"Got 'button_dr' pressed. APP_STATUS={APP_STATUS}")
   time.sleep_ms(200)
   if APP_STATUS=="dr":
    print("Setting status to 'None'")
    APP_STATUS=None
    color_neostrip(neostrip,"nocolor",config["neopixel"]["count"])
   else:
    print("Setting status to 'dr'")
    APP_STATUS="dr"
    color_neostrip(neostrip,"red",config["neopixel"]["count"])
