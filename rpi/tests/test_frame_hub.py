import asyncio

from camera.frame_hub import MJPEG_HEADER, FrameHub


async def test_fans_out_one_frame_to_multiple_clients():
    hub = FrameHub()
    streams = [hub.mjpeg_frames(), hub.mjpeg_frames()]
    waiting = [asyncio.create_task(anext(stream)) for stream in streams]

    await asyncio.sleep(0)
    await hub.publish(b"jpeg-data")

    expected = MJPEG_HEADER + b"jpeg-data\r\n"
    assert await asyncio.gather(*waiting) == [expected, expected]

    await asyncio.gather(*(stream.aclose() for stream in streams))


async def test_slow_client_skips_to_latest_frame():
    hub = FrameHub()
    stream = hub.mjpeg_frames()

    await hub.publish(b"first")
    assert await anext(stream) == MJPEG_HEADER + b"first\r\n"

    await hub.publish(b"second")
    await hub.publish(b"latest")
    assert await anext(stream) == MJPEG_HEADER + b"latest\r\n"

    await stream.aclose()
