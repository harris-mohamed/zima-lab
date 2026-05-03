import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class PlantReading:
    ts: int
    plant_id: int
    ph: Optional[float]
    tds: Optional[float]
    water_temp: Optional[float]
    water_level_cm: Optional[float]
    air_temp: Optional[float]
    humidity: Optional[float]


NUM_PLANTS = 5


def parse_line(line: str) -> Optional[list[PlantReading]]:
    """Parse a JSON line from the Arduino into one PlantReading per plant.

    Arduino sends flat keys: ph_0..ph_4, tds_0..tds_4, wt_0..wt_4, wl_0..wl_4
    plus shared at (air temp) and hm (humidity).
    Returns None if the line is malformed or missing ts.
    Sensor values of -1.0 are converted to None.
    """
    try:
        data = json.loads(line.strip())
    except (json.JSONDecodeError, ValueError):
        return None

    ts = data.get("ts")
    if ts is None:
        return None

    def _val(key: str) -> Optional[float]:
        v = data.get(key)
        if v is None or v < 0:
            return None
        return float(v)

    air_temp = _val("at")
    humidity = _val("hm")

    return [
        PlantReading(
            ts=int(ts),
            plant_id=i,
            ph=_val(f"ph_{i}"),
            tds=_val(f"tds_{i}"),
            water_temp=_val(f"wt_{i}"),
            water_level_cm=_val(f"wl_{i}"),
            air_temp=air_temp,
            humidity=humidity,
        )
        for i in range(NUM_PLANTS)
    ]
