from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_session
from db import queries
from db.models import SensorReading

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


def _reading_to_dict(r: SensorReading) -> dict:
    return {
        "id": r.id,
        "recorded_at": r.recorded_at.isoformat(),
        "ph": r.ph,
        "tds": r.tds,
        "water_temp": r.water_temp,
        "air_temp": r.air_temp,
        "humidity": r.humidity,
        "water_level_cm": r.water_level_cm,
    }


@router.get("/latest")
async def get_latest(session: Annotated[AsyncSession, Depends(get_session)]):
    reading = await queries.get_latest(session)
    if reading is None:
        return {}
    return _reading_to_dict(reading)


@router.get("/history")
async def get_history(
    session: Annotated[AsyncSession, Depends(get_session)],
    minutes: int = Query(default=60, ge=1, le=1440),
):
    readings = await queries.get_history(session, minutes=minutes)
    return [_reading_to_dict(r) for r in readings]
