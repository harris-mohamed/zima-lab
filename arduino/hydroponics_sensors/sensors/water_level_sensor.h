#pragma once
#include <Arduino.h>

class WaterLevelSensor {
public:
    WaterLevelSensor(uint8_t trig_pin, uint8_t echo_pin, float tank_height_cm);
    void begin();
    // Returns water depth in cm (tank_height - measured distance), or -1.0 on timeout.
    float read();

private:
    uint8_t _trig;
    uint8_t _echo;
    float _tank_height;
};
