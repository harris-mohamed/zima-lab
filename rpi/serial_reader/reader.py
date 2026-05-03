import asyncio
import logging

import serial

from config.settings import settings
from db.writer import write_sensor_reading
from serial_reader.parser import parse_line

logger = logging.getLogger(__name__)


async def run_serial_reader(session_factory, hub) -> None:
    """Long-running asyncio task: read serial lines, persist to DB, broadcast to WebSocket clients."""
    loop = asyncio.get_event_loop()

    def _open_port():
        return serial.Serial(settings.serial_port, settings.serial_baud, timeout=2)

    ser = None
    while True:
        try:
            if ser is None or not ser.is_open:
                ser = await loop.run_in_executor(None, _open_port)
                logger.info("Serial port %s opened", settings.serial_port)

            raw = await loop.run_in_executor(None, ser.readline)
            line = raw.decode("utf-8", errors="ignore")
            reading = parse_line(line)
            if reading is None:
                continue

            async with session_factory() as session:
                await write_sensor_reading(session, reading)

            await hub.broadcast(reading)

        except serial.SerialException as exc:
            logger.warning("Serial error: %s — retrying in 5s", exc)
            if ser and ser.is_open:
                ser.close()
            ser = None
            await asyncio.sleep(5)
        except Exception as exc:
            logger.exception("Unexpected error in serial reader: %s", exc)
            await asyncio.sleep(1)
