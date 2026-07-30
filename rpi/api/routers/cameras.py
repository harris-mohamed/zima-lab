from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from camera.picam_stream import picam_mjpeg_frames
from camera.snapshot import SNAPSHOT_DIR
from camera.usb_cam_stream import usb_mjpeg_frames

router = APIRouter(prefix="/api/cameras", tags=["cameras"])

STREAM_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate",
    "Pragma": "no-cache",
}


@router.get("/picam")
async def stream_picam():
    return StreamingResponse(
        picam_mjpeg_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers=STREAM_HEADERS,
    )


@router.get("/usb")
async def stream_usb():
    return StreamingResponse(
        usb_mjpeg_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers=STREAM_HEADERS,
    )


@router.get("/snapshots")
async def list_snapshots():
    """Return all saved snapshots, newest first."""
    files = sorted(SNAPSHOT_DIR.glob("*.jpg"), reverse=True)
    result = []
    for f in files:
        source = f.name.split("_")[0]
        ts_str = f.stem[len(source) + 1 :]  # strip "picam_" / "usb_"
        try:
            taken_at = (
                datetime.strptime(ts_str, "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc).isoformat()
            )
        except ValueError:
            taken_at = None
        result.append({"filename": f.name, "source": source, "taken_at": taken_at})
    return result


@router.get("/snapshots/{filename}")
async def get_snapshot(filename: str):
    """Serve a single saved snapshot by filename."""
    # Guard against path traversal
    if "/" in filename or "\\" in filename or not filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Invalid filename")
    path = SNAPSHOT_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return FileResponse(path, media_type="image/jpeg")
