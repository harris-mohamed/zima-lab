import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

import cv2

from camera.lock import picam_lock
from config.settings import settings

logger = logging.getLogger(__name__)

SNAPSHOT_DIR = Path(__file__).parent.parent.parent / "data" / "snapshots"
INTERVAL_S   = 30 * 60   # 30 minutes
KEEP_LAST    = 48         # 24 hours of snapshots per source


def _rotate(source: str) -> None:
    files = sorted(SNAPSHOT_DIR.glob(f"{source}_*.jpg"))
    for f in files[:-KEEP_LAST]:
        f.unlink(missing_ok=True)


def capture_usb(ts: str) -> None:
    cap = cv2.VideoCapture(settings.usb_cam_index)
    if not cap.isOpened():
        logger.warning("Snapshot: USB camera unavailable (stream may be active)")
        return
    for _ in range(5):   # warmup frames so exposure settles
        cap.read()
    ret, frame = cap.read()
    cap.release()
    if not ret:
        logger.warning("Snapshot: USB camera read failed")
        return
    path = SNAPSHOT_DIR / f"usb_{ts}.jpg"
    cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    logger.info("Snapshot saved: %s", path.name)
    _rotate("usb")


def capture_picam(ts: str) -> None:
    try:
        from picamera2 import Picamera2
    except ImportError:
        logger.warning("Snapshot: picamera2 not available")
        return
    try:
        cam = Picamera2()
        cam.start()
        path = SNAPSHOT_DIR / f"picam_{ts}.jpg"
        cam.capture_file(str(path))
        cam.stop()
        cam.close()
        logger.info("Snapshot saved: %s", path.name)
        _rotate("picam")
    except Exception as exc:
        logger.warning("Snapshot: Pi camera failed (%s) — stream may be active", exc)


async def run_snapshot_task() -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    loop = asyncio.get_running_loop()
    while True:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        await loop.run_in_executor(None, capture_usb, ts)
        async with picam_lock:
            await loop.run_in_executor(None, capture_picam, ts)
        await asyncio.sleep(INTERVAL_S)
