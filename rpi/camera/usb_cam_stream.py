import asyncio
import logging
from time import monotonic

import cv2

from camera.frame_hub import usb_hub
from config.settings import settings

logger = logging.getLogger(__name__)

FPS = 5
FRAME_INTERVAL_S = 1 / FPS
MAX_READ_FAILURES = 10
RETRY_DELAY_S = 5
WARMUP_FRAMES = 10


def _camera_source() -> int | str:
    device = settings.usb_cam_device
    return int(device) if device.isdigit() else device


def _open_camera():
    capture = cv2.VideoCapture(_camera_source())
    if not capture.isOpened():
        capture.release()
        return None

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Let UVC cameras negotiate their native frame rate. Some webcams, including
    # C270 variants, return black frames when forced to an unsupported low FPS.
    for _ in range(WARMUP_FRAMES):
        capture.read()
    return capture


def _read_jpeg(capture) -> bytes | None:
    ok, frame = capture.read()
    if not ok:
        return None
    ok, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return jpeg.tobytes() if ok else None


async def run_usb_capture() -> None:
    """Open the USB camera once and continually publish its latest JPEG."""
    while True:
        capture = None
        try:
            capture = await asyncio.to_thread(_open_camera)
            if capture is None:
                raise RuntimeError(f"could not open USB camera at {settings.usb_cam_device}")

            logger.info("USB camera capture started at 640x480, %d FPS", FPS)
            failures = 0
            while failures < MAX_READ_FAILURES:
                started = monotonic()
                jpeg = await asyncio.to_thread(_read_jpeg, capture)
                if jpeg is None:
                    failures += 1
                    logger.warning("USB camera read failed (%d/%d)", failures, MAX_READ_FAILURES)
                else:
                    failures = 0
                    await usb_hub.publish(jpeg)
                elapsed = monotonic() - started
                await asyncio.sleep(max(0, FRAME_INTERVAL_S - elapsed))

            raise RuntimeError("too many consecutive USB camera read failures")
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("USB camera capture failed; retrying in %d seconds", RETRY_DELAY_S)
        finally:
            if capture is not None:
                await asyncio.to_thread(capture.release)
        await asyncio.sleep(RETRY_DELAY_S)


def usb_mjpeg_frames():
    return usb_hub.mjpeg_frames()
