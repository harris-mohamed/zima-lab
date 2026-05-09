/* ----------------------------------------------------------
       HumiditySensor
       DHT11 air temperature and humidity driver
   ---------------------------------------------------------- */
#include "sensors/humidity_sensor.h"

HumiditySensor::HumiditySensor(uint8_t pin) : _dht(pin, DHT11) {}

void HumiditySensor::begin() {
  _dht.begin();
}

static inline bool is_nan(float v) {
  uint32_t bits;
  memcpy(&bits, &v, sizeof(bits));
  return (bits & 0x7FFFFFFF) > 0x7F800000;
}

AirReading HumiditySensor::read() {
  AirReading r;
  r.temp_f   = _dht.readTemperature(true);
  r.humidity = _dht.readHumidity();
  if (is_nan(r.temp_f))   r.temp_f   = -1.0f;
  if (is_nan(r.humidity)) r.humidity = -1.0f;
  return r;
}
