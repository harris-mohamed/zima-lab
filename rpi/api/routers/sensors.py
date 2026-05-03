from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_session
from db import queries
from db.models import SensorReading

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


def _reading_to_dict(r: SensorReading) -> dict:
    return {
        "recorded_at": r.recorded_at.isoformat(),
        "plant_id": r.plant_id,
        "ph": r.ph,
        "tds": r.tds,
        "water_temp": r.water_temp,
        "water_level_cm": r.water_level_cm,
        "air_temp": r.air_temp,
        "humidity": r.humidity,
    }


@router.get("/latest")
async def get_latest(session: Annotated[AsyncSession, Depends(get_session)]):
    readings = await queries.get_latest_per_plant(session)
    return [_reading_to_dict(r) for r in readings]


@router.get("/history")
async def get_history(
    session: Annotated[AsyncSession, Depends(get_session)],
    minutes: int = Query(default=60, ge=1, le=1440),
):
    readings = await queries.get_history(session, minutes=minutes)
    return [_reading_to_dict(r) for r in readings]
