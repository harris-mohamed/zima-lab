import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers import cameras
from camera.snapshot import run_snapshot_task

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    snapshot_task = asyncio.create_task(run_snapshot_task(), name="snapshot")
    logger.info("Camera snapshot task started")

    yield

    snapshot_task.cancel()
    try:
        await snapshot_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Zima Lab Camera API", lifespan=lifespan)

app.include_router(cameras.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
