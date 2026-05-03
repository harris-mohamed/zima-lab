import pytest
from sqlalchemy import select

from db.models import SensorReading
from db.writer import write_sensor_reading
from serial_reader.parser import SensorReading as ParsedReading


@pytest.mark.asyncio
async def test_write_and_read(session):
    reading = ParsedReading(
        ts=12345,
        ph=6.5,
        tds=800.0,
        water_temp=22.0,
        air_temp=25.0,
        humidity=65.0,
        water_level_cm=15.0,
    )
    await write_sensor_reading(session, reading)

    result = await session.execute(
        select(SensorReading).where(SensorReading.arduino_ts == 12345)
    )
    row = result.scalar_one()
    assert row.ph == pytest.approx(6.5)
    assert row.tds == pytest.approx(800.0)


@pytest.mark.asyncio
async def test_null_values_stored(session):
    reading = ParsedReading(
        ts=99999,
        ph=None,
        tds=None,
        water_temp=None,
        air_temp=24.0,
        humidity=70.0,
        water_level_cm=10.0,
    )
    await write_sensor_reading(session, reading)

    result = await session.execute(
        select(SensorReading).where(SensorReading.arduino_ts == 99999)
    )
    row = result.scalar_one()
    assert row.ph is None
    assert row.tds is None
    assert row.air_temp == pytest.approx(24.0)
