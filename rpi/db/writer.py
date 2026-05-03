from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import SensorReading as SensorReadingModel
from serial_reader.parser import SensorReading


async def write_sensor_reading(session: AsyncSession, reading: SensorReading) -> None:
    row = SensorReadingModel(
        recorded_at=datetime.now(timezone.utc),
        arduino_ts=reading.ts,
        ph=reading.ph,
        tds=reading.tds,
        water_temp=reading.water_temp,
        air_temp=reading.air_temp,
        humidity=reading.humidity,
        water_level_cm=reading.water_level_cm,
    )
    session.add(row)
    await session.commit()
