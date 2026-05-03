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

// Per-plant sensors
PhSensor          ph_0(PH_PIN_0), ph_1(PH_PIN_1), ph_2(PH_PIN_2),
                  ph_3(PH_PIN_3), ph_4(PH_PIN_4);
TdsSensor         tds_0(TDS_PIN_0), tds_1(TDS_PIN_1), tds_2(TDS_PIN_2),
                  tds_3(TDS_PIN_3), tds_4(TDS_PIN_4);
TemperatureSensor wt_0(WATER_TEMP_PIN_0), wt_1(WATER_TEMP_PIN_1),
                  wt_2(WATER_TEMP_PIN_2), wt_3(WATER_TEMP_PIN_3),
                  wt_4(WATER_TEMP_PIN_4);
WaterLevelSensor  wl_0(TRIG_PIN_0, ECHO_PIN_0, TANK_HEIGHT_CM),
                  wl_1(TRIG_PIN_1, ECHO_PIN_1, TANK_HEIGHT_CM),
                  wl_2(TRIG_PIN_2, ECHO_PIN_2, TANK_HEIGHT_CM),
                  wl_3(TRIG_PIN_3, ECHO_PIN_3, TANK_HEIGHT_CM),
                  wl_4(TRIG_PIN_4, ECHO_PIN_4, TANK_HEIGHT_CM);

// Pointer arrays for looping
PhSensor*         ph_sensors[NUM_PLANTS]  = {&ph_0,  &ph_1,  &ph_2,  &ph_3,  &ph_4};
TdsSensor*        tds_sensors[NUM_PLANTS] = {&tds_0, &tds_1, &tds_2, &tds_3, &tds_4};
TemperatureSensor* wt_sensors[NUM_PLANTS] = {&wt_0,  &wt_1,  &wt_2,  &wt_3,  &wt_4};
WaterLevelSensor* wl_sensors[NUM_PLANTS]  = {&wl_0,  &wl_1,  &wl_2,  &wl_3,  &wl_4};

// Shared sensor
HumiditySensor air(DHT_PIN);

/*--- SETUP ---*/
void setup() {
  Serial.begin(SERIAL_BAUD);

  for (int i = 0; i < NUM_PLANTS; i++) {
    ph_sensors[i]->begin();
    tds_sensors[i]->begin();
    wt_sensors[i]->begin();
    wl_sensors[i]->begin();
  }
  air.begin();
}

void loop() {
  AirReading ar = air.read();

  // Build JSON incrementally into a 512-byte buffer.
  char buf[512];
  int  n = 0;

  n += snprintf(buf + n, sizeof(buf) - n,
    "{\"ts\":%lu,\"at\":%.2f,\"hm\":%.1f",
    millis() / 1000UL, ar.temp_c, ar.humidity);

  for (int i = 0; i < NUM_PLANTS; i++) {
    float wtemp   = wt_sensors[i]->read();
    float tds_ppm = tds_sensors[i]->read(wtemp > 0 ? wtemp : 25.0f);

    n += snprintf(buf + n, sizeof(buf) - n,
      ",\"ph_%d\":%.2f,\"tds_%d\":%.1f,\"wt_%d\":%.2f,\"wl_%d\":%.1f",
      i, ph_sensors[i]->read(),
      i, tds_ppm,
      i, wtemp,
      i, wl_sensors[i]->read());
  }

  n += snprintf(buf + n, sizeof(buf) - n, "}");
  Serial.println(buf);

  delay(SAMPLE_INTERVAL);
}
