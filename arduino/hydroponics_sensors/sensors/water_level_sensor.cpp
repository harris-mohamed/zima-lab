#include "water_level_sensor.h"

WaterLevelSensor::WaterLevelSensor(uint8_t trig_pin, uint8_t echo_pin, float tank_height_cm)
    : _trig(trig_pin), _echo(echo_pin), _tank_height(tank_height_cm) {}

void WaterLevelSensor::begin() {
    pinMode(_trig, OUTPUT);
    pinMode(_echo, INPUT);
}

float WaterLevelSensor::read() {
    digitalWrite(_trig, LOW);
    delayMicroseconds(2);
    digitalWrite(_trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(_trig, LOW);

    // pulseIn timeout: 30ms covers ~5m max range; realistic tank max is ~1m.
    long duration = pulseIn(_echo, HIGH, 30000);
    if (duration == 0) return -1.0f;

    float distance_cm = duration * 0.0343f / 2.0f;
    float level = _tank_height - distance_cm;
    if (level < 0.0f) level = 0.0f;
    return level;
}
