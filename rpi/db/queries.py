from datetime import datetime, timedelta, timezone
from typing import Optional

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import SensorReading


async def get_latest_per_plant(session: AsyncSession) -> list[SensorReading]:
    """Return the most recent reading for each plant."""
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=5)
    result = await session.execute(
        select(SensorReading)
        .where(SensorReading.recorded_at >= cutoff)
        .order_by(SensorReading.plant_id.asc(), SensorReading.recorded_at.desc())
    )
    rows = result.scalars().all()

    # Keep only the most recent row per plant_id
    seen: set[int] = set()
    latest = []
    for row in rows:
        if row.plant_id not in seen:
            seen.add(row.plant_id)
            latest.append(row)
    return latest


async def get_history(session: AsyncSession, minutes: int = 60) -> list[SensorReading]:
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    result = await session.execute(
        select(SensorReading)
        .where(SensorReading.recorded_at >= cutoff)
        .order_by(SensorReading.recorded_at.asc(), SensorReading.plant_id.asc())
    )
    return list(result.scalars().all())


async def export_dataframe(
    session: AsyncSession,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
) -> pd.DataFrame:
    stmt = select(SensorReading).order_by(SensorReading.recorded_at.asc())
    if start:
        stmt = stmt.where(SensorReading.recorded_at >= start)
    if end:
        stmt = stmt.where(SensorReading.recorded_at <= end)

    result = await session.execute(stmt)
    rows = result.scalars().all()

    data = [
        {
            "recorded_at": r.recorded_at,
            "plant_id": r.plant_id,
            "ph": r.ph,
            "tds": r.tds,
            "water_temp": r.water_temp,
            "water_level_cm": r.water_level_cm,
            "air_temp": r.air_temp,
            "humidity": r.humidity,
        }
        for r in rows
    ]
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.set_index("recorded_at")
    return df
