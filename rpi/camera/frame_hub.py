import asyncio
from collections.abc import AsyncGenerator

MJPEG_HEADER = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"


class FrameHub:
    """Keep one latest JPEG frame and fan it out to any number of clients."""

    def __init__(self) -> None:
        self._condition = asyncio.Condition()
        self._frame: bytes | None = None
        self._version = 0

    async def publish(self, frame: bytes) -> None:
        async with self._condition:
            self._frame = frame
            self._version += 1
            self._condition.notify_all()

    def latest(self) -> bytes | None:
        return self._frame

    async def wait_for_frame(self, timeout: float = 15) -> bytes | None:
        if self._frame is not None:
            return self._frame
        try:
            async with asyncio.timeout(timeout):
                async with self._condition:
                    await self._condition.wait_for(lambda: self._frame is not None)
                    return self._frame
        except TimeoutError:
            return None

    async def mjpeg_frames(self) -> AsyncGenerator[bytes, None]:
        version = -1
        while True:
            async with self._condition:
                await self._condition.wait_for(
                    lambda: self._frame is not None and self._version != version
                )
                frame = self._frame
                version = self._version
            if frame is not None:
                yield MJPEG_HEADER + frame + b"\r\n"


picam_hub = FrameHub()
usb_hub = FrameHub()
