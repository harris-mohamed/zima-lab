#pragma once
#include <Arduino.h>
#include <DHT.h>

struct AirReading {
    float temp_c;     // -1.0 on error
    float humidity;   // -1.0 on error
};

class HumiditySensor {
public:
    explicit HumiditySensor(uint8_t pin);
    void begin();
    AirReading read();

private:
    DHT _dht;
};
