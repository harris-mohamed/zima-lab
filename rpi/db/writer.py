from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import SensorReading as SensorReadingModel
from serial_reader.parser import PlantReading


async def write_plant_readings(session: AsyncSession, readings: list[PlantReading]) -> None:
    now = datetime.now(timezone.utc)
    for reading in readings:
        session.add(SensorReadingModel(
            recorded_at=now,
            arduino_ts=reading.ts,
            plant_id=reading.plant_id,
            ph=reading.ph,
            tds=reading.tds,
            water_temp=reading.water_temp,
            water_level_cm=reading.water_level_cm,
            air_temp=reading.air_temp,
            humidity=reading.humidity,
        ))
    await session.commit()
