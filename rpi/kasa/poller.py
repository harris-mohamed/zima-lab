import asyncio
import logging
from datetime import datetime, timezone

from kasa import SmartStrip

from config.settings import settings
from influx.writer import OutletData, write_outlets

logger = logging.getLogger(__name__)


async def run_kasa_poller() -> None:
    if not settings.kasa_host:
        logger.info("KASA_HOST not configured — skipping Kasa poller")
        return

    strip: SmartStrip | None = None

    while True:
        try:
            if strip is None:
                strip = SmartStrip(settings.kasa_host)

            await strip.update()
            ts = datetime.now(timezone.utc)

            outlets = [
                OutletData(
                    outlet_id=i,
                    outlet_name=plug.alias or f"Outlet {i}",
                    watts=float(plug.emeter_realtime.power or 0),
                    voltage=float(plug.emeter_realtime.voltage or 0),
                    current_a=float(plug.emeter_realtime.current or 0),
                    total_kwh=float(plug.emeter_realtime.total or 0),
                    ts=ts,
                )
                for i, plug in enumerate(strip.children)
            ]

            await write_outlets(outlets)
            logger.debug("Wrote %d outlet readings", len(outlets))

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning("Kasa poll error: %s — retrying in 30s", exc)
            strip = None
            await asyncio.sleep(30)
            continue

        await asyncio.sleep(settings.kasa_poll_interval)
