/* ----------------------------------------------------------
       ZIMA LAB - pH Probe Calibration Test
       Configuration (trimmed copy of hydroponics_sensors/config.h
       — only what the pH driver needs)
   ---------------------------------------------------------- */
#pragma once

/* ----------------------------------------------------------
       pH SENSOR PIN (analog)
   ---------------------------------------------------------- */
#define PH_PIN_0   A0

/* ----------------------------------------------------------
       SERIAL
   ---------------------------------------------------------- */
#define SERIAL_BAUD  115200

/* ----------------------------------------------------------
       pH CALIBRATION (2-point: buffer pH 4.0 and pH 7.0)
       Update these after running this test, then copy back
       into hydroponics_sensors/config.h
   ---------------------------------------------------------- */
#define PH_CAL_SLOPE      -5.70f
#define PH_CAL_INTERCEPT  21.34f
