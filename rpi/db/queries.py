from datetime import datetime, timedelta, timezone
from typing import Optional

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import SensorReading


async def get_latest(session: AsyncSession) -> Optional[SensorReading]:
    result = await session.execute(
        select(SensorReading).order_by(SensorReading.recorded_at.desc()).limit(1)
    )
    return result.scalar_one_or_none()


async def get_history(session: AsyncSession, minutes: int = 60) -> list[SensorReading]:
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    result = await session.execute(
        select(SensorReading)
        .where(SensorReading.recorded_at >= cutoff)
        .order_by(SensorReading.recorded_at.asc())
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
            "ph": r.ph,
            "tds": r.tds,
            "water_temp": r.water_temp,
            "air_temp": r.air_temp,
            "humidity": r.humidity,
            "water_level_cm": r.water_level_cm,
        }
        for r in rows
    ]
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.set_index("recorded_at")
    return df
