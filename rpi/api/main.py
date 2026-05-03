import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers import cameras, export, sensors
from api.websocket import router as ws_router
from broadcast.hub import hub
from db.database import AsyncSessionLocal, engine
from db.models import Base
from serial_reader.reader import run_serial_reader

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    serial_task = asyncio.create_task(
        run_serial_reader(AsyncSessionLocal, hub),
        name="serial-reader",
    )
    logger.info("Serial reader task started")

    yield

    serial_task.cancel()
    try:
        await serial_task
    except asyncio.CancelledError:
        pass
    await engine.dispose()


app = FastAPI(title="Zima Lab API", lifespan=lifespan)

app.include_router(sensors.router)
app.include_router(cameras.router)
app.include_router(export.router)
app.include_router(ws_router)

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
