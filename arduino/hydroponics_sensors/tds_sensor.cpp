/* ----------------------------------------------------------
       TdsSensor
       TDS probe driver (analog, temperature-compensated)
   ---------------------------------------------------------- */
#include "sensors/tds_sensor.h"
#include "config.h"

/* ----------------------------------------------------------
   Function:      TdsSensor
   Description:   Constructor — stores pin number
   Inputs:        pin — analog pin number
   Outputs:       None
   ---------------------------------------------------------- */
TdsSensor::TdsSensor(uint8_t pin) : _pin(pin) {}

/* ----------------------------------------------------------
   Function:      begin
   Description:   Configures the analog pin as INPUT
   Inputs:        None
   Outputs:       None
   ---------------------------------------------------------- */
void TdsSensor::begin() {
  pinMode(_pin, INPUT);
}

/* ----------------------------------------------------------
   Function:      read
   Description:   Averages SAMPLE_COUNT ADC readings, applies
                  temperature compensation, and returns TDS in ppm
   Inputs:        water_temp_c — water temperature in degrees C
   Outputs:       TDS in ppm, or -1.0 on invalid result
   ---------------------------------------------------------- */
float TdsSensor::read(float water_temp_c) {
  long sum = 0;
  for (int i = 0; i < SAMPLE_COUNT; i++) {
    sum += analogRead(_pin);
    delay(10);
  }
  float voltage = (sum / (float)SAMPLE_COUNT) * (TDS_VREF / (TDS_ADC_BITS - 1));

  float comp_coeff   = 1.0f + 0.02f * (water_temp_c - 25.0f);
  float comp_voltage = voltage / comp_coeff;

  float tds = (133.42f * comp_voltage * comp_voltage * comp_voltage
             - 255.86f * comp_voltage * comp_voltage
             + 857.39f * comp_voltage) * 0.5f;

  if (tds < 0.0f) return -1.0f;
  return tds;
}
