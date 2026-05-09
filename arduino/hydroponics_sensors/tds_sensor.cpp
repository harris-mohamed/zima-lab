/* ----------------------------------------------------------
       TdsSensor
       TDS probe driver (analog, temperature-compensated)
   ---------------------------------------------------------- */
#include "sensors/tds_sensor.h"
#include "config.h"
#include <string.h>

TdsSensor::TdsSensor(uint8_t pin)
  : _pin(pin), _bufIdx(0), _lastSample(0)
{
  memset(_buf, 0, sizeof(_buf));
}

void TdsSensor::begin() {
  pinMode(_pin, INPUT);
}

/* ----------------------------------------------------------
   Function:      update
   Description:   Samples ADC into circular buffer every 40ms.
                  Call on every loop() iteration.
   ---------------------------------------------------------- */
void TdsSensor::update() {
  if (millis() - _lastSample > 40U) {
    _lastSample = millis();
    _buf[_bufIdx++] = analogRead(_pin);
    if (_bufIdx == SCOUNT) _bufIdx = 0;
  }
}

/* ----------------------------------------------------------
   Function:      read
   Description:   Applies median filter over the current buffer,
                  temperature-compensates, and returns TDS in ppm.
   Inputs:        water_temp_c — water temperature in degrees C
   Outputs:       TDS in ppm, or -1.0 on invalid result
   ---------------------------------------------------------- */
float TdsSensor::read(float water_temp_c) {
  int tmp[SCOUNT];
  memcpy(tmp, _buf, sizeof(tmp));

  float voltage = _getMedianNum(tmp, SCOUNT) * (TDS_VREF / (TDS_ADC_BITS - 1));

  float comp_coeff   = 1.0f + 0.02f * (water_temp_c - 25.0f);
  float comp_voltage = voltage / comp_coeff;

  float tds = (133.42f * comp_voltage * comp_voltage * comp_voltage
             - 255.86f * comp_voltage * comp_voltage
             + 857.39f * comp_voltage) * 0.5f;

  return tds < 0.0f ? -1.0f : tds;
}

/* ----------------------------------------------------------
   Function:      _getMedianNum
   Description:   Bubble-sort + median pick (DFRobot reference)
   ---------------------------------------------------------- */
int TdsSensor::_getMedianNum(int arr[], int len) {
  int tmp[len];
  for (int i = 0; i < len; i++) tmp[i] = arr[i];

  for (int j = 0; j < len - 1; j++) {
    for (int i = 0; i < len - j - 1; i++) {
      if (tmp[i] > tmp[i + 1]) {
        int t      = tmp[i];
        tmp[i]     = tmp[i + 1];
        tmp[i + 1] = t;
      }
    }
  }

  return (len & 1) ? tmp[(len - 1) / 2]
                   : (tmp[len / 2] + tmp[len / 2 - 1]) / 2;
}
