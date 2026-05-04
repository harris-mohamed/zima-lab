/* ----------------------------------------------------------
       WaterLevelSensor
       HC-SR04 ultrasonic water level driver
   ---------------------------------------------------------- */
#include "sensors/water_level_sensor.h"

/* ----------------------------------------------------------
   Function:      WaterLevelSensor
   Description:   Constructor — stores pin numbers and tank height
   Inputs:        trig_pin      — HC-SR04 trigger pin
                  echo_pin      — HC-SR04 echo pin
                  tank_height_cm — full tank depth in cm
   Outputs:       None
   ---------------------------------------------------------- */
WaterLevelSensor::WaterLevelSensor(uint8_t trig_pin, uint8_t echo_pin, float tank_height_cm)
  : _trig(trig_pin), _echo(echo_pin), _tank_height(tank_height_cm) {}

/* ----------------------------------------------------------
   Function:      begin
   Description:   Configures trigger as OUTPUT and echo as INPUT
   Inputs:        None
   Outputs:       None
   ---------------------------------------------------------- */
void WaterLevelSensor::begin() {
  pinMode(_trig, OUTPUT);
  pinMode(_echo, INPUT);
}

/* ----------------------------------------------------------
   Function:      read
   Description:   Fires the HC-SR04 and returns water depth as
                  tank_height minus measured distance
   Inputs:        None
   Outputs:       Water depth in cm, or -1.0 on echo timeout
   ---------------------------------------------------------- */
float WaterLevelSensor::read() {
  digitalWrite(_trig, LOW);
  delayMicroseconds(2);
  digitalWrite(_trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(_trig, LOW);

  long duration = pulseIn(_echo, HIGH, 30000);
  if (duration == 0) return -1.0f;

  float distance_cm = duration * 0.0343f / 2.0f;
  float level = _tank_height - distance_cm;
  if (level < 0.0f) level = 0.0f;
  return level;
}
