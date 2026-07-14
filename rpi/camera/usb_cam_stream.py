import asyncio
import logging
from typing import AsyncGenerator

import cv2

from config.settings import settings

logger = logging.getLogger(__name__)

MAX_READ_FAILURES = 30


def _camera_source() -> int | str:
    device = settings.usb_cam_device
    if device.isdigit():
        return int(device)
    return device


def _open_camera():
    cap = cv2.VideoCapture(_camera_source())
    if not cap.isOpened():
        cap.release()
        return None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap


def _read_jpeg(cap) -> bytes | None:
    ret, frame = cap.read()
    if not ret:
        return None

    ok, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    if not ok:
        return None
    return jpeg.tobytes()


async def usb_mjpeg_frames() -> AsyncGenerator[bytes, None]:
    """Yield MJPEG frames from the USB webcam using OpenCV."""
    cap = await asyncio.to_thread(_open_camera)
    if cap is None:
        logger.error("Could not open USB camera at %s", settings.usb_cam_device)
        return

    failures = 0
    try:
        while True:
            jpeg = await asyncio.to_thread(_read_jpeg, cap)
            if jpeg is None:
                failures += 1
                logger.warning("USB camera read failed; retrying")
                if failures >= MAX_READ_FAILURES:
                    logger.error("USB camera failed %d times; closing stream", failures)
                    return
                await asyncio.sleep(1)
                continue

            failures = 0
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n"
            )
            await asyncio.sleep(1 / 15)
    finally:
        await asyncio.to_thread(cap.release)
