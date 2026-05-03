from fastapi import APIRouter, Query

from influx.queries import get_latest_outlet_power, get_power_history

router = APIRouter(prefix="/api/power", tags=["power"])


@router.get("/latest")
async def latest_power():
    return await get_latest_outlet_power()


@router.get("/history")
async def power_history(minutes: int = Query(default=60, ge=1, le=1440)):
    return await get_power_history(minutes=minutes)
