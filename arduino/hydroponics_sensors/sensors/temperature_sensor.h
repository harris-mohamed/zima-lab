#pragma once
#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

class TemperatureSensor {
public:
    explicit TemperatureSensor(uint8_t pin);
    void begin();
    // Returns water temperature in °C, or -1.0 on read error / device not found.
    float read();

private:
    OneWire _wire;
    DallasTemperature _sensors;
};
