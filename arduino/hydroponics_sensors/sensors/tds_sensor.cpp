#include "tds_sensor.h"
#include "../config.h"

TdsSensor::TdsSensor(uint8_t pin) : _pin(pin) {}

void TdsSensor::begin() {
    pinMode(_pin, INPUT);
}

float TdsSensor::read(float water_temp_c) {
    long sum = 0;
    for (int i = 0; i < SAMPLE_COUNT; i++) {
        sum += analogRead(_pin);
        delay(10);
    }
    float voltage = (sum / (float)SAMPLE_COUNT) * (TDS_VREF / (TDS_ADC_BITS - 1));

    // Temperature compensation: normalize to 25°C baseline.
    float comp_coeff = 1.0f + 0.02f * (water_temp_c - 25.0f);
    float comp_voltage = voltage / comp_coeff;

    // Standard TDS formula from DFRobot application note.
    float tds = (133.42f * comp_voltage * comp_voltage * comp_voltage
               - 255.86f * comp_voltage * comp_voltage
               + 857.39f * comp_voltage) * 0.5f;

    if (tds < 0.0f) return -1.0f;
    return tds;
}
