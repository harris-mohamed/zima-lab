import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

from camera.frame_hub import FrameHub, picam_hub, usb_hub

logger = logging.getLogger(__name__)

SNAPSHOT_DIR = Path(__file__).parent.parent.parent / "data" / "snapshots"
INTERVAL_S = 30 * 60  # 30 minutes
KEEP_LAST = 48  # 24 hours of snapshots per source


def _save_snapshot(source: str, timestamp: str, frame: bytes) -> None:
    path = SNAPSHOT_DIR / f"{source}_{timestamp}.jpg"
    path.write_bytes(frame)
    logger.info("Snapshot saved: %s", path.name)

    files = sorted(SNAPSHOT_DIR.glob(f"{source}_*.jpg"))
    for old_file in files[:-KEEP_LAST]:
        old_file.unlink(missing_ok=True)


async def _save_latest(source: str, hub: FrameHub, timestamp: str) -> None:
    frame = await hub.wait_for_frame()
    if frame is None:
        logger.warning("Snapshot: %s camera has not produced a frame", source)
        return
    await asyncio.to_thread(_save_snapshot, source, timestamp, frame)


async def run_snapshot_task() -> None:
    """Archive the shared frames without reopening either physical camera."""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    while True:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        await asyncio.gather(
            _save_latest("picam", picam_hub, timestamp),
            _save_latest("usb", usb_hub, timestamp),
        )
        await asyncio.sleep(INTERVAL_S)
