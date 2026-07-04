/* ----------------------------------------------------------
       ZIMA LAB - pH Probe Calibration Test

       Standalone sketch — verifies (or re-derives) PH_CAL_SLOPE
       and PH_CAL_INTERCEPT before wiring the pH probe back into
       hydroponics_sensors.ino. Uses the same PhSensor driver as
       the main sketch.

       Procedure:
         1. Rinse probe in distilled water.
         2. Dip in pH 7.0 buffer, wait ~30-60s for the reading
            to stabilize, record the printed voltage as V7.
         3. Rinse, dip in pH 4.0 buffer, record voltage as V4.
         4. slope     = (7.0 - 4.0) / (V7 - V4)
            intercept = 7.0 - slope * V7
         5. Copy the new values into PH_CAL_SLOPE / PH_CAL_INTERCEPT
            in both this config.h and hydroponics_sensors/config.h.
   ---------------------------------------------------------- */

#include "config.h"
#include "sensors/ph_sensor.h"

PhSensor ph(PH_PIN_0);

const int SAMPLE_COUNT = 10;

float readRawVoltage() {
  long sum = 0;
  for (int i = 0; i < SAMPLE_COUNT; i++) {
    sum += analogRead(PH_PIN_0);
    delay(10);
  }
  return (sum / (float)SAMPLE_COUNT) * (5.0f / 1023.0f);
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  ph.begin();
  Serial.println(F("pH Probe Calibration Test"));
  Serial.println(F("Rinse probe in distilled water between buffers."));
  Serial.println(F("Dip in pH 7.0 buffer first, then pH 4.0."));
  Serial.println(F("voltage_V -> pH (using current PH_CAL_SLOPE/INTERCEPT)"));
}

void loop() {
  float voltage  = readRawVoltage();
  float phValue  = ph.read();

  Serial.print(voltage, 3);
  Serial.print(F(" V  ->  pH "));
  Serial.println(phValue, 2);

  delay(1000);
}
