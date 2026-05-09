/* ----------------------------------------------------------
       ZIMA LAB - Hydroponics Sensor Node

       Harris M

       May 3, 2026
   ---------------------------------------------------------- */

/* ----------------------------------------------------------
       LIBRARIES
   ---------------------------------------------------------- */
#include "config.h"
// #include "sensors/ph_sensor.h"   // pH probe not connected
#include "sensors/tds_sensor.h"
#include "sensors/temperature_sensor.h"
#include "sensors/humidity_sensor.h"
#include "sensors/water_level_sensor.h"

/* ----------------------------------------------------------
       GLOBAL VARIABLES
   ---------------------------------------------------------- */

// Per-plant sensors
/* PhSensor ph_0(PH_PIN_0), ph_1(PH_PIN_1), ph_2(PH_PIN_2),
             ph_3(PH_PIN_3), ph_4(PH_PIN_4); */
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
/* PhSensor* ph_sensors[NUM_PLANTS] = {&ph_0, &ph_1, &ph_2, &ph_3, &ph_4}; */
TdsSensor*        tds_sensors[NUM_PLANTS] = {&tds_0, &tds_1, &tds_2, &tds_3, &tds_4};
TemperatureSensor* wt_sensors[NUM_PLANTS] = {&wt_0,  &wt_1,  &wt_2,  &wt_3,  &wt_4};
WaterLevelSensor* wl_sensors[NUM_PLANTS]  = {&wl_0,  &wl_1,  &wl_2,  &wl_3,  &wl_4};

// Shared sensor
HumiditySensor air(DHT_PIN);

/*--- SETUP ---*/
void setup() {
  Serial.begin(SERIAL_BAUD);

  for (int i = 0; i < NUM_PLANTS; i++) {
    tds_sensors[i]->begin();
    wt_sensors[i]->begin();
    wl_sensors[i]->begin();
  }
  air.begin();
}

void loop() {
  // Fill TDS circular buffers (samples every 40ms, non-blocking)
  for (int i = 0; i < NUM_PLANTS; i++)
    tds_sensors[i]->update();

  // Emit JSON once per SAMPLE_INTERVAL
  static unsigned long lastEmit = 0;
  if (millis() - lastEmit < SAMPLE_INTERVAL) return;
  lastEmit = millis();

  AirReading ar = air.read();

  // AVR snprintf does not support %f — use dtostrf for every float value.
  char buf[512];
  char f[10];
  int  n = 0;

  n += snprintf(buf + n, sizeof(buf) - n, "{\"ts\":%lu", millis() / 1000UL);

  dtostrf(ar.temp_f,  1, 2, f); n += snprintf(buf + n, sizeof(buf) - n, ",\"at\":%s", f);
  dtostrf(ar.humidity,1, 1, f); n += snprintf(buf + n, sizeof(buf) - n, ",\"hm\":%s", f);

  for (int i = 0; i < NUM_PLANTS; i++) {
    float wtemp   = wt_sensors[i]->read();
    float tds_ppm = tds_sensors[i]->read(wtemp > 0 ? wtemp : 25.0f);

    dtostrf(tds_ppm,           1, 1, f); n += snprintf(buf + n, sizeof(buf) - n, ",\"tds_%d\":%s", i, f);
    dtostrf(wtemp,             1, 2, f); n += snprintf(buf + n, sizeof(buf) - n, ",\"wt_%d\":%s",  i, f);
    dtostrf(wl_sensors[i]->read(), 1, 1, f); n += snprintf(buf + n, sizeof(buf) - n, ",\"wl_%d\":%s",  i, f);
  }

  n += snprintf(buf + n, sizeof(buf) - n, "}");
  Serial.println(buf);
}
