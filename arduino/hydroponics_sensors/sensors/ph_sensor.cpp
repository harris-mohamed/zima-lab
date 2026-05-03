#include "ph_sensor.h"
#include "../config.h"

PhSensor::PhSensor(uint8_t pin)
    : _pin(pin), _slope(PH_CAL_SLOPE), _intercept(PH_CAL_INTERCEPT) {}

void PhSensor::begin() {
    pinMode(_pin, INPUT);
}

float PhSensor::read() {
    // Average multiple samples to reduce ADC noise.
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
