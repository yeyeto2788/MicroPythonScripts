# MicroWeatherStation

This script will read the sensor DHT11 data and it will create a simple server so the data is shown on a web page.

### Image of code running on the Wemos D1 mini board:

<p align="center">
<img src="../../static/images/weather_station_index.png" alt="Drawing"  width="500"/>
</p>

## Parts needed:

  * ESP8266

  I'm using the Wemos D1 Mini board.

  <p align="center">
  <img src="../../static/images/wemos_d1_mini.png" alt="Wemos d1 mini board"  width="200"/>
  </p>

  * DHT11 Sensor

  <p align="center">
  <img src="../../static/images/dht11.png" alt="DHT11 Sensor"  width="200"/>
  </p>

## NOTE:

Take into account that I'm using a Wemos D1 mini and it's DHT11 shield, so in the script you'll see the **`d = dht.DHT11(machine.Pin(2))`** and in the example page of the Micropython documentation they use other pin (4).

### TO DO:

- [ ] Better documentation.

- [x] Add execution images.
