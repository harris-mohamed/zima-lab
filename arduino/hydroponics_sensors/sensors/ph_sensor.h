/* ----------------------------------------------------------
       PhSensor
       pH probe driver (analog, 2-point calibrated)
   ---------------------------------------------------------- */
#pragma once
#include <Arduino.h>

/* ----------------------------------------------------------
       CLASS DEFINITION
   ---------------------------------------------------------- */
class PhSensor {
public:
  explicit PhSensor(uint8_t pin);
  void  begin();
  float read();

private:
  uint8_t _pin;
  float   _slope;
  float   _intercept;
  static constexpr int SAMPLE_COUNT = 10;
};
