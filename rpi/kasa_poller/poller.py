import asyncio
import logging
from datetime import datetime, timezone

from kasa import Device, Discover, Module

from config.settings import settings
from influx.writer import OutletData, write_outlets

logger = logging.getLogger(__name__)


async def run_kasa_poller() -> None:
    if not settings.kasa_host:
        logger.info("KASA_HOST not configured — skipping Kasa poller")
        return

    device: Device | None = None

    while True:
        try:
            if device is None:
                device = await Discover.discover_single(
                    settings.kasa_host,
                    username=settings.kasa_username,
                    password=settings.kasa_password,
                )

            await device.update()
            ts = datetime.now(timezone.utc)

            outlets = [
                OutletData(
                    outlet_id=i,
                    outlet_name=child.alias or f"Outlet {i}",
                    watts=float(child.modules[Module.Energy].current_consumption or 0),
                    voltage=float(child.modules[Module.Energy].voltage or 0),
                    current_a=float(child.modules[Module.Energy].current or 0),
                    total_kwh=float(child.modules[Module.Energy].consumption_total or 0),
                    ts=ts,
                )
                for i, child in enumerate(device.children)
            ]

            await write_outlets(outlets)
            logger.debug("Wrote %d outlet readings", len(outlets))

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning("Kasa poll error: %s — retrying in 30s", exc)
            device = None
            await asyncio.sleep(30)
            continue

        await asyncio.sleep(settings.kasa_poll_interval)
