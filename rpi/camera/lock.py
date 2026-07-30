import asyncio

# Picamera2 only allows one open instance at a time; the live stream
# (picam_stream.py) and the periodic snapshot task (snapshot.py) must
# take turns rather than racing for the hardware.
picam_lock = asyncio.Lock()

# Same constraint applies to the USB webcam (V4L2 only allows one
# exclusive handle) — the live stream (usb_cam_stream.py) and the
# periodic snapshot task (snapshot.py) must take turns here too.
usb_cam_lock = asyncio.Lock()
