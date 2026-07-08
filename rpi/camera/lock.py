import asyncio

# Picamera2 only allows one open instance at a time; the live stream
# (picam_stream.py) and the periodic snapshot task (snapshot.py) must
# take turns rather than racing for the hardware.
picam_lock = asyncio.Lock()
