#pragma once

// ── Pin assignments ────────────────────────────────────────────────────────
#define PH_PIN            A0
#define TDS_PIN           A1
#define WATER_TEMP_PIN    2    // DS18B20 OneWire data
#define DHT_PIN           3    // DHT22 data
#define TRIG_PIN          4    // HC-SR04 trigger
#define ECHO_PIN          5    // HC-SR04 echo

// ── Serial ─────────────────────────────────────────────────────────────────
#define SERIAL_BAUD       115200
#define SAMPLE_INTERVAL   1000   // ms between readings

// ── pH calibration (2-point: buffer pH 4.0 and pH 7.0) ────────────────────
// Measure the ADC voltage at each buffer and solve:  pH = slope * voltage + intercept
// Default values are typical for a DFRobot SEN0161-style probe; recalibrate for yours.
#define PH_CAL_SLOPE      -5.70f
#define PH_CAL_INTERCEPT  21.34f

// ── TDS calibration ────────────────────────────────────────────────────────
#define TDS_VREF          5.0f    // Arduino supply voltage
#define TDS_ADC_BITS      1024    // 10-bit ADC

// ── Water level (HC-SR04) ──────────────────────────────────────────────────
#define TANK_HEIGHT_CM    30.0f  // full tank depth in cm; water_level = height - distance
