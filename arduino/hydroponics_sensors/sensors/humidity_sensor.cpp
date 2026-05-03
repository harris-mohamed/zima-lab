/* ----------------------------------------------------------
       HumiditySensor
       DHT22 air temperature and humidity driver
   ---------------------------------------------------------- */
#include "humidity_sensor.h"

/* ----------------------------------------------------------
   Function:      HumiditySensor
   Description:   Constructor — initializes DHT22 on given pin
   Inputs:        pin — digital data pin number
   Outputs:       None
   ---------------------------------------------------------- */
HumiditySensor::HumiditySensor(uint8_t pin) : _dht(pin, DHT22) {}

/* ----------------------------------------------------------
   Function:      begin
   Description:   Starts the DHT library
   Inputs:        None
   Outputs:       None
   ---------------------------------------------------------- */
void HumiditySensor::begin() {
  _dht.begin();
}

/* ----------------------------------------------------------
   Function:      read
   Description:   Reads air temperature and humidity from the DHT22
   Inputs:        None
   Outputs:       AirReading struct with temp_c and humidity fields;
                  either field is -1.0 if the sensor returns NaN
   ---------------------------------------------------------- */
AirReading HumiditySensor::read() {
  AirReading r;
  r.temp_c   = _dht.readTemperature();
  r.humidity = _dht.readHumidity();
  if (isnan(r.temp_c))   r.temp_c   = -1.0f;
  if (isnan(r.humidity)) r.humidity = -1.0f;
  return r;
}
