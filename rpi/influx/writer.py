import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from config.settings import settings

logger = logging.getLogger(__name__)

_client: InfluxDBClient | None = None
_write_api = None


@dataclass
class OutletData:
    outlet_id: int
    outlet_name: str
    watts: float
    voltage: float
    current_a: float
    total_kwh: float
    ts: datetime


def _get_write_api():
    global _client, _write_api
    if _client is None:
        _client = InfluxDBClient(
            url=settings.influx_url,
            token=settings.influx_token,
            org=settings.influx_org,
        )
        _write_api = _client.write_api(write_options=SYNCHRONOUS)
    return _write_api


def _write_sync(outlets: list[OutletData]) -> None:
    points = [
        Point("outlet_power")
        .tag("outlet_id", str(o.outlet_id))
        .tag("outlet_name", o.outlet_name)
        .field("watts", o.watts)
        .field("voltage", o.voltage)
        .field("current_a", o.current_a)
        .field("total_kwh", o.total_kwh)
        .time(o.ts, WritePrecision.SECONDS)
        for o in outlets
    ]
    _get_write_api().write(bucket=settings.influx_bucket, record=points)


async def write_outlets(outlets: list[OutletData]) -> None:
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _write_sync, outlets)


def close() -> None:
    global _client
    if _client:
        _client.close()
        _client = None
