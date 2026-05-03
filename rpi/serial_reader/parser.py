import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class SensorReading:
    ts: int
    ph: Optional[float]
    tds: Optional[float]
    water_temp: Optional[float]
    air_temp: Optional[float]
    humidity: Optional[float]
    water_level_cm: Optional[float]


def parse_line(line: str) -> Optional[SensorReading]:
    """Parse a JSON line from the Arduino serial stream into a SensorReading.

    Returns None if the line is malformed or missing required fields.
    Sensor values of -1.0 (error/disconnected) are converted to None.
    """
    try:
        data = json.loads(line.strip())
    except (json.JSONDecodeError, ValueError):
        return None

    def _val(key: str) -> Optional[float]:
        v = data.get(key)
        if v is None or v < 0:
            return None
        return float(v)

    ts = data.get("ts")
    if ts is None:
        return None

    return SensorReading(
        ts=int(ts),
        ph=_val("ph"),
        tds=_val("tds"),
        water_temp=_val("water_temp"),
        air_temp=_val("air_temp"),
        humidity=_val("humidity"),
        water_level_cm=_val("water_level_cm"),
    )
