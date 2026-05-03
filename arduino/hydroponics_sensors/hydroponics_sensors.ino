/* ----------------------------------------------------------
       ZIMA LAB - Hydroponics Sensor Node

       Harris M

       May 3, 2026
   ---------------------------------------------------------- */

/* ----------------------------------------------------------
       LIBRARIES
   ---------------------------------------------------------- */
#include "config.h"
#include "sensors/ph_sensor.h"
#include "sensors/tds_sensor.h"
#include "sensors/temperature_sensor.h"
#include "sensors/humidity_sensor.h"
#include "sensors/water_level_sensor.h"

/* ----------------------------------------------------------
       GLOBAL VARIABLES
   ---------------------------------------------------------- */
PhSensor          ph(PH_PIN);
TdsSensor         tds(TDS_PIN);
TemperatureSensor water_temp(WATER_TEMP_PIN);
HumiditySensor    air(DHT_PIN);
WaterLevelSensor  level(TRIG_PIN, ECHO_PIN, TANK_HEIGHT_CM);

/*--- SETUP ---*/
void setup() {
  Serial.begin(SERIAL_BAUD);
  ph.begin();
  tds.begin();
  water_temp.begin();
  air.begin();
  level.begin();
}

void loop() {
  float wtemp   = water_temp.read();
  AirReading ar = air.read();

  float tds_ppm = tds.read(wtemp > 0 ? wtemp : 25.0f);

  char buf[128];
  snprintf(buf, sizeof(buf),
    "{\"ts\":%lu,\"ph\":%.2f,\"tds\":%.1f,"
    "\"water_temp\":%.2f,\"air_temp\":%.2f,"
    "\"humidity\":%.1f,\"water_level_cm\":%.1f}",
    millis() / 1000UL,
    ph.read(),
    tds_ppm,
    wtemp,
    ar.temp_c,
    ar.humidity,
    level.read()
  );
  Serial.println(buf);

  delay(SAMPLE_INTERVAL);
}
