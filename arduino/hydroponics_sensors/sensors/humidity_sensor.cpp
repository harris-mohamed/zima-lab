#include "humidity_sensor.h"

HumiditySensor::HumiditySensor(uint8_t pin) : _dht(pin, DHT22) {}

void HumiditySensor::begin() {
    _dht.begin();
}

AirReading HumiditySensor::read() {
    AirReading r;
    r.temp_c   = _dht.readTemperature();
    r.humidity = _dht.readHumidity();
    if (isnan(r.temp_c))   r.temp_c   = -1.0f;
    if (isnan(r.humidity)) r.humidity = -1.0f;
    return r;
}
