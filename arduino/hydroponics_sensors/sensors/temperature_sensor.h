/* ----------------------------------------------------------
       TemperatureSensor
       DS18B20 OneWire water temperature driver
   ---------------------------------------------------------- */
#pragma once
#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

/* ----------------------------------------------------------
       CLASS DEFINITION
   ---------------------------------------------------------- */
class TemperatureSensor {
public:
  explicit TemperatureSensor(uint8_t pin);
  void  begin();
  float read();

private:
  OneWire          _wire;
  DallasTemperature _sensors;
};
