/* ----------------------------------------------------------
       TdsSensor
       TDS probe driver (analog, temperature-compensated)
   ---------------------------------------------------------- */
#pragma once
#include <Arduino.h>

/* ----------------------------------------------------------
       CLASS DEFINITION
   ---------------------------------------------------------- */
class TdsSensor {
public:
  explicit TdsSensor(uint8_t pin);
  void  begin();
  float read(float water_temp_c = 25.0f);

private:
  uint8_t _pin;
  static constexpr int SAMPLE_COUNT = 10;
};
