import io
import logging
from typing import AsyncGenerator

logger = logging.getLogger(__name__)


async def picam_mjpeg_frames() -> AsyncGenerator[bytes, None]:
    """Yield MJPEG frames from the Pi Camera Module using picamera2."""
    try:
        from picamera2 import Picamera2
        from picamera2.encoders import MJPEGEncoder
        from picamera2.outputs import FileOutput
    except ImportError:
        logger.warning("picamera2 not available; Pi camera stream disabled")
        return

    cam = Picamera2()
    config = cam.create_video_configuration(main={"size": (1280, 720)})
    cam.configure(config)

    output = io.BytesIO()
    encoder = MJPEGEncoder()
    file_output = FileOutput(output)
    cam.start_recording(encoder, file_output)

    try:
        while True:
            output.seek(0)
            frame = output.read()
            if frame:
                output.seek(0)
                output.truncate()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            import asyncio
            await asyncio.sleep(1 / 15)
    finally:
        cam.stop_recording()
        cam.close()
