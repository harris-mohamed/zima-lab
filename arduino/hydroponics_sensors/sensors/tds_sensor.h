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
  void  update();                           // call every loop iteration
  float read(float water_temp_c = 25.0f);  // returns median-filtered value

private:
  uint8_t       _pin;
  static constexpr int SCOUNT = 30;
  int           _buf[SCOUNT];
  int           _bufIdx;
  unsigned long _lastSample;

  static int _getMedianNum(int arr[], int len);
};
