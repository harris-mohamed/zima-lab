"""
Standalone ML data export script.

Usage:
    uv run python -m ml.export --out ../data/exports/dataset.parquet
    uv run python -m ml.export --start 2026-01-01 --end 2026-02-01 --out data.csv
"""

import argparse
import asyncio
from datetime import datetime
from pathlib import Path

from db.database import AsyncSessionLocal
from db.queries import export_dataframe


async def _export(start, end, out: Path):
    async with AsyncSessionLocal() as session:
        df = await export_dataframe(session, start=start, end=end)

    if df.empty:
        print("No data found for the specified range.")
        return

    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix == ".parquet":
        df.to_parquet(out)
    else:
        df.to_csv(out)
    print(f"Exported {len(df)} rows to {out}")


def main():
    parser = argparse.ArgumentParser(description="Export sensor data for ML")
    parser.add_argument("--start", type=datetime.fromisoformat, default=None)
    parser.add_argument("--end", type=datetime.fromisoformat, default=None)
    parser.add_argument("--out", type=Path, default=Path("../data/exports/dataset.parquet"))
    args = parser.parse_args()
    asyncio.run(_export(args.start, args.end, args.out))


if __name__ == "__main__":
    main()
