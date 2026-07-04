/* ----------------------------------------------------------
       PhSensor
       pH probe driver (analog, 2-point calibrated)
   ---------------------------------------------------------- */
#include "sensors/ph_sensor.h"
#include "config.h"

/* ----------------------------------------------------------
   Function:      PhSensor
   Description:   Constructor — stores pin and calibration constants
   Inputs:        pin — analog pin number
   Outputs:       None
   ---------------------------------------------------------- */
PhSensor::PhSensor(uint8_t pin)
  : _pin(pin), _slope(PH_CAL_SLOPE), _intercept(PH_CAL_INTERCEPT) {}

/* ----------------------------------------------------------
   Function:      begin
   Description:   Configures the analog pin as INPUT
   Inputs:        None
   Outputs:       None
   ---------------------------------------------------------- */
void PhSensor::begin() {
  pinMode(_pin, INPUT);
}

/* ----------------------------------------------------------
   Function:      read
   Description:   Averages SAMPLE_COUNT ADC readings and returns
                  the calibrated pH value
   Inputs:        None
   Outputs:       pH (0.0–14.0), or -1.0 on out-of-range result
   ---------------------------------------------------------- */
float PhSensor::read() {
  long sum = 0;
  for (int i = 0; i < SAMPLE_COUNT; i++) {
    sum += analogRead(_pin);
    delay(10);
  }
  float voltage = (sum / (float)SAMPLE_COUNT) * (5.0f / 1023.0f);
  float ph = _slope * voltage + _intercept;
  if (ph < 0.0f || ph > 14.0f) return -1.0f;
  return ph;
}
