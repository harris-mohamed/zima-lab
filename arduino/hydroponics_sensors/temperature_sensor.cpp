/* ----------------------------------------------------------
       TemperatureSensor
       DS18B20 OneWire water temperature driver
   ---------------------------------------------------------- */
#include "sensors/temperature_sensor.h"

/* ----------------------------------------------------------
   Function:      TemperatureSensor
   Description:   Constructor — initializes OneWire bus and sensor
   Inputs:        pin — OneWire data pin number
   Outputs:       None
   ---------------------------------------------------------- */
TemperatureSensor::TemperatureSensor(uint8_t pin)
  : _wire(pin), _sensors(&_wire) {}

/* ----------------------------------------------------------
   Function:      begin
   Description:   Starts the DallasTemperature library
   Inputs:        None
   Outputs:       None
   ---------------------------------------------------------- */
void TemperatureSensor::begin() {
  _sensors.begin();
}

/* ----------------------------------------------------------
   Function:      read
   Description:   Requests a temperature conversion and returns
                  the result from the first device on the bus
   Inputs:        None
   Outputs:       Temperature in degrees C, or -1.0 on error
   ---------------------------------------------------------- */
float TemperatureSensor::read() {
  _sensors.requestTemperatures();
  float temp = _sensors.getTempCByIndex(0);
  if (temp < -100.0f) return -1.0f;
  return temp;
}
