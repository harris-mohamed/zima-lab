import asyncio
import logging

from influxdb_client import InfluxDBClient

from config.settings import settings

logger = logging.getLogger(__name__)

_client: InfluxDBClient | None = None


def _get_client() -> InfluxDBClient:
    global _client
    if _client is None:
        _client = InfluxDBClient(
            url=settings.influx_url,
            token=settings.influx_token,
            org=settings.influx_org,
        )
    return _client


def _latest_sync() -> list[dict]:
    query_api = _get_client().query_api()
    flux = f"""
from(bucket: "{settings.influx_bucket}")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "outlet_power")
  |> last()
"""
    tables = query_api.query(flux)

    outlets: dict[str, dict] = {}
    for table in tables:
        for rec in table.records:
            oid = str(rec.values.get("outlet_id", "?"))
            if oid not in outlets:
                outlets[oid] = {
                    "outlet_id": int(oid) if oid.isdigit() else oid,
                    "outlet_name": rec.values.get("outlet_name", ""),
                    "recorded_at": rec.get_time().isoformat(),
                }
            outlets[oid][rec.get_field()] = rec.get_value()

    return sorted(outlets.values(), key=lambda r: r["outlet_id"])


def _history_sync(minutes: int) -> list[dict]:
    query_api = _get_client().query_api()
    flux = f"""
from(bucket: "{settings.influx_bucket}")
  |> range(start: -{minutes}m)
  |> filter(fn: (r) => r._measurement == "outlet_power" and r._field == "watts")
  |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
  |> sort(columns: ["_time"])
"""
    tables = query_api.query(flux)

    results = []
    for table in tables:
        for rec in table.records:
            results.append({
                "time": rec.get_time().isoformat(),
                "outlet_id": str(rec.values.get("outlet_id", "")),
                "outlet_name": str(rec.values.get("outlet_name", "")),
                "watts": rec.get_value(),
            })
    return results


async def get_latest_outlet_power() -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _latest_sync)


async def get_power_history(minutes: int = 60) -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _history_sync, minutes)
