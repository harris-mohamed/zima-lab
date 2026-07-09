import asyncio
import logging
from typing import AsyncGenerator

import cv2

from config.settings import settings

logger = logging.getLogger(__name__)


async def usb_mjpeg_frames() -> AsyncGenerator[bytes, None]:
    """Yield MJPEG frames from the USB webcam using OpenCV."""
    cap = cv2.VideoCapture(settings.usb_cam_device)
    if not cap.isOpened():
        logger.error("Could not open USB camera at %s", settings.usb_cam_device)
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.warning("USB camera read failed; retrying")
                await asyncio.sleep(0.1)
                continue

            _, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n"
            )
            await asyncio.sleep(1 / 15)
    finally:
        cap.release()
