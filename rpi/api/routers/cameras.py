from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from camera.picam_stream import picam_mjpeg_frames
from camera.usb_cam_stream import usb_mjpeg_frames

router = APIRouter(prefix="/api/cameras", tags=["cameras"])


@router.get("/picam")
async def stream_picam():
    return StreamingResponse(
        picam_mjpeg_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.get("/usb")
async def stream_usb():
    return StreamingResponse(
        usb_mjpeg_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
