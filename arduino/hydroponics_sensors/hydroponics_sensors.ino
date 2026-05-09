/* ----------------------------------------------------------
       ZIMA LAB - Hydroponics Sensor Node

       Harris M

       May 3, 2026
   ---------------------------------------------------------- */

#include "config.h"
#include "sensors/humidity_sensor.h"
#include "sensors/tds_sensor.h"

HumiditySensor air(DHT_PIN);
TdsSensor      tds(TDS_PIN_0);

void setup() {
  Serial.begin(SERIAL_BAUD);
  air.begin();
  tds.begin();
}

void loop() {
  tds.update();  // fill 30-sample buffer every 40ms

  static unsigned long lastEmit = 0;
  if (millis() - lastEmit < SAMPLE_INTERVAL) return;
  lastEmit = millis();

  AirReading ar = air.read();

  // AVR snprintf does not support %f — use dtostrf for float values.
  char buf[128];
  char f[10];
  int  n = 0;

  n += snprintf(buf + n, sizeof(buf) - n, "{\"ts\":%lu", millis() / 1000UL);
  dtostrf(ar.temp_f,   1, 2, f); n += snprintf(buf + n, sizeof(buf) - n, ",\"at\":%s", f);
  dtostrf(ar.humidity, 1, 1, f); n += snprintf(buf + n, sizeof(buf) - n, ",\"hm\":%s", f);
  dtostrf(tds.read(),  1, 1, f); n += snprintf(buf + n, sizeof(buf) - n, ",\"tds_0\":%s", f);
  n += snprintf(buf + n, sizeof(buf) - n, "}");

  Serial.println(buf);
}
