/* ----------------------------------------------------------
       WaterLevelSensor
       HC-SR04 ultrasonic water level driver
   ---------------------------------------------------------- */
#pragma once
#include <Arduino.h>

/* ----------------------------------------------------------
       CLASS DEFINITION
   ---------------------------------------------------------- */
class WaterLevelSensor {
public:
  WaterLevelSensor(uint8_t trig_pin, uint8_t echo_pin, float tank_height_cm);
  void  begin();
  float read();

private:
  uint8_t _trig;
  uint8_t _echo;
  float   _tank_height;
};
