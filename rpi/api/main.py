import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers import cameras
from camera.picam_stream import run_picam_capture
from camera.snapshot import run_snapshot_task
from camera.usb_cam_stream import run_usb_capture

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    tasks = (
        asyncio.create_task(run_picam_capture(), name="picam-capture"),
        asyncio.create_task(run_usb_capture(), name="usb-capture"),
        asyncio.create_task(run_snapshot_task(), name="snapshot"),
    )
    logger.info("Shared camera capture and snapshot tasks started")

    yield

    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


app = FastAPI(title="Zima Lab Camera API", lifespan=lifespan)

app.include_router(cameras.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
