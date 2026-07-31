import asyncio
import logging
from time import monotonic

import cv2

from camera.frame_hub import picam_hub

logger = logging.getLogger(__name__)

FPS = 5
FRAME_INTERVAL_S = 1 / FPS
RETRY_DELAY_S = 5


def _capture_jpeg(camera) -> bytes | None:
    frame = camera.capture_array("main")
    ok, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return jpeg.tobytes() if ok else None


async def run_picam_capture() -> None:
    """Open the Pi camera once and continually publish its latest JPEG."""
    try:
        from picamera2 import Picamera2
    except ImportError:
        logger.error("picamera2 not available; Pi camera capture disabled")
        return

    while True:
        camera = None
        try:
            camera = Picamera2()
            config = camera.create_video_configuration(
                main={"size": (1280, 720), "format": "RGB888"},
                controls={"FrameRate": float(FPS)},
            )
            camera.configure(config)
            camera.start()
            logger.info("Pi camera capture started at 1280x720, %d FPS", FPS)

            while True:
                started = monotonic()
                jpeg = await asyncio.to_thread(_capture_jpeg, camera)
                if jpeg is not None:
                    await picam_hub.publish(jpeg)
                elapsed = monotonic() - started
                await asyncio.sleep(max(0, FRAME_INTERVAL_S - elapsed))
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Pi camera capture failed; retrying in %d seconds", RETRY_DELAY_S)
        finally:
            if camera is not None:
                try:
                    await asyncio.to_thread(camera.stop)
                except Exception:
                    logger.debug("Pi camera was already stopped", exc_info=True)
                try:
                    await asyncio.to_thread(camera.close)
                except Exception:
                    logger.debug("Pi camera close failed", exc_info=True)
        await asyncio.sleep(RETRY_DELAY_S)


def picam_mjpeg_frames():
    return picam_hub.mjpeg_frames()
