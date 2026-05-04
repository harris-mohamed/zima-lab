/* ----------------------------------------------------------
       HumiditySensor
       DHT11 air temperature and humidity driver
   ---------------------------------------------------------- */
#include "sensors/humidity_sensor.h"

/* ----------------------------------------------------------
   Function:      HumiditySensor
   Description:   Constructor — initializes DHT22 on given pin
   Inputs:        pin — digital data pin number
   Outputs:       None
   ---------------------------------------------------------- */
HumiditySensor::HumiditySensor(uint8_t pin) : _dht(pin, DHT11) {}

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
static inline bool is_nan(float v) {
  uint32_t bits;
  memcpy(&bits, &v, sizeof(bits));
  return (bits & 0x7FFFFFFF) > 0x7F800000;
}

AirReading HumiditySensor::read() {
  AirReading r;
  r.temp_c   = _dht.readTemperature();
  r.humidity = _dht.readHumidity();
  if (is_nan(r.temp_c))   r.temp_c   = -1.0f;
  if (is_nan(r.humidity)) r.humidity = -1.0f;
  return r;
}
