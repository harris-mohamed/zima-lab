import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers import cameras, export, power, sensors
from api.websocket import router as ws_router
from broadcast.hub import hub
from db.database import AsyncSessionLocal, engine
from db.models import Base
from camera.snapshot import run_snapshot_task
from influx.writer import close as close_influx
from kasa_poller.poller import run_kasa_poller
from serial_reader.reader import run_serial_reader

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    serial_task   = asyncio.create_task(run_serial_reader(AsyncSessionLocal, hub), name="serial-reader")
    kasa_task     = asyncio.create_task(run_kasa_poller(),   name="kasa-poller")
    snapshot_task = asyncio.create_task(run_snapshot_task(), name="snapshot")
    logger.info("Serial reader, Kasa poller, and snapshot tasks started")

    yield

    for task in (serial_task, kasa_task, snapshot_task):
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    close_influx()
    await engine.dispose()


app = FastAPI(title="Zima Lab API", lifespan=lifespan)

app.include_router(sensors.router)
app.include_router(cameras.router)
app.include_router(export.router)
app.include_router(power.router)
app.include_router(ws_router)

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
