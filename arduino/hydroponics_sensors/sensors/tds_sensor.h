#pragma once
#include <Arduino.h>

class TdsSensor {
public:
    explicit TdsSensor(uint8_t pin);
    void begin();
    // Returns TDS in ppm, temperature-compensated. Pass water_temp in °C.
    // Returns -1.0 on read error.
    float read(float water_temp_c = 25.0f);

private:
    uint8_t _pin;
    static constexpr int SAMPLE_COUNT = 10;
};
