#pragma once
#include <Arduino.h>

class PhSensor {
public:
    explicit PhSensor(uint8_t pin);
    void begin();
    // Returns pH value (4.0–10.0), or -1.0 on read error.
    float read();

private:
    uint8_t _pin;
    float _slope;
    float _intercept;
    static constexpr int SAMPLE_COUNT = 10;
};
