import io
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_session
from db.queries import export_dataframe

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/csv")
async def export_csv(
    session: Annotated[AsyncSession, Depends(get_session)],
    start: Optional[datetime] = Query(default=None),
    end: Optional[datetime] = Query(default=None),
):
    df = await export_dataframe(session, start=start, end=end)
    csv_bytes = df.to_csv().encode()
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sensor_data.csv"},
    )


@router.get("/parquet")
async def export_parquet(
    session: Annotated[AsyncSession, Depends(get_session)],
    start: Optional[datetime] = Query(default=None),
    end: Optional[datetime] = Query(default=None),
):
    df = await export_dataframe(session, start=start, end=end)
    buf = io.BytesIO()
    df.to_parquet(buf, index=True)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=sensor_data.parquet"},
    )
