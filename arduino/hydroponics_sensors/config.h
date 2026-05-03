/* ----------------------------------------------------------
       ZIMA LAB - Hydroponics Sensor Node
       Configuration
   ---------------------------------------------------------- */
#pragma once

/* ----------------------------------------------------------
       PLANT COUNT
   ---------------------------------------------------------- */
#define NUM_PLANTS  5

/* ----------------------------------------------------------
       pH SENSOR PINS (analog)
   ---------------------------------------------------------- */
#define PH_PIN_0   A0
#define PH_PIN_1   A1
#define PH_PIN_2   A2
#define PH_PIN_3   A3
#define PH_PIN_4   A4

/* ----------------------------------------------------------
       TDS SENSOR PINS (analog)
   ---------------------------------------------------------- */
#define TDS_PIN_0  A5
#define TDS_PIN_1  A6
#define TDS_PIN_2  A7
#define TDS_PIN_3  A8
#define TDS_PIN_4  A9

/* ----------------------------------------------------------
       WATER TEMP PINS (DS18B20 OneWire, one per plant)
   ---------------------------------------------------------- */
#define WATER_TEMP_PIN_0  22
#define WATER_TEMP_PIN_1  23
#define WATER_TEMP_PIN_2  24
#define WATER_TEMP_PIN_3  25
#define WATER_TEMP_PIN_4  26

/* ----------------------------------------------------------
       WATER LEVEL PINS (HC-SR04, trigger + echo per plant)
   ---------------------------------------------------------- */
#define TRIG_PIN_0  27
#define ECHO_PIN_0  28
#define TRIG_PIN_1  29
#define ECHO_PIN_1  30
#define TRIG_PIN_2  31
#define ECHO_PIN_2  32
#define TRIG_PIN_3  33
#define ECHO_PIN_3  34
#define TRIG_PIN_4  35
#define ECHO_PIN_4  36

/* ----------------------------------------------------------
       SHARED SENSORS
   ---------------------------------------------------------- */
#define DHT_PIN    3    // DHT11 data (one per grow space)

/* ----------------------------------------------------------
       SERIAL
   ---------------------------------------------------------- */
#define SERIAL_BAUD      115200
#define SAMPLE_INTERVAL  1000   // ms between readings

/* ----------------------------------------------------------
       pH CALIBRATION (2-point: buffer pH 4.0 and pH 7.0)
   ---------------------------------------------------------- */
#define PH_CAL_SLOPE      -5.70f
#define PH_CAL_INTERCEPT  21.34f

/* ----------------------------------------------------------
       TDS CALIBRATION
   ---------------------------------------------------------- */
#define TDS_VREF      5.0f    // Arduino supply voltage
#define TDS_ADC_BITS  1024    // 10-bit ADC

/* ----------------------------------------------------------
       WATER LEVEL (HC-SR04)
   ---------------------------------------------------------- */
#define TANK_HEIGHT_CM  30.0f   // full tank depth in cm
