#include "temperature_sensor.h"

TemperatureSensor::TemperatureSensor(uint8_t pin)
    : _wire(pin), _sensors(&_wire) {}

void TemperatureSensor::begin() {
    _sensors.begin();
}

float TemperatureSensor::read() {
    _sensors.requestTemperatures();
    float temp = _sensors.getTempCByIndex(0);
    // DallasTemperature returns DEVICE_DISCONNECTED_C (-127) on error.
    if (temp < -100.0f) return -1.0f;
    return temp;
}
