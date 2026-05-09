/* ----------------------------------------------------------
       HumiditySensor
       DHT11 air temperature and humidity driver
   ---------------------------------------------------------- */
#pragma once
#include <Arduino.h>
#include <DHT.h>

/* ----------------------------------------------------------
       STRUCTS
   ---------------------------------------------------------- */
struct AirReading {
  float temp_f;    // -1.0 on error
  float humidity;  // -1.0 on error
};

/* ----------------------------------------------------------
       CLASS DEFINITION
   ---------------------------------------------------------- */
class HumiditySensor {
public:
  explicit HumiditySensor(uint8_t pin);
  void       begin();
  AirReading read();

private:
  DHT _dht;
};
