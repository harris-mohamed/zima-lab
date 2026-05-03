# Zima Lab — Automated Hydroponics Monitor

Raspberry Pi + Arduino MEGA hydroponic monitoring system with a live React dashboard.

## Hardware

- **Raspberry Pi** — runs the Python backend, camera streams, and serves the dashboard
- **Arduino MEGA** — reads analog sensors (pH, TDS, water temp, air temp/humidity, water level) and sends JSON over serial
- **Pi Camera Module** — overhead crop view (MJPEG stream)
- **USB Webcam** — secondary view (MJPEG stream)

## Directory Structure

```
arduino/   — Arduino sketch and sensor drivers
rpi/       — Python backend (FastAPI, SQLAlchemy, serial reader)
frontend/  — React + Vite dashboard
data/      — gitignored runtime data (DB, exports)
```

## Quick Start

### 1. Flash the Arduino

Open `arduino/hydroponics_sensors/hydroponics_sensors.ino` in the Arduino IDE and upload to the MEGA. Open the Serial Monitor at 115200 baud to verify JSON output.

### 2. Set up the database

Install PostgreSQL and create the database:

```bash
createdb zimalab
createuser zima
psql -c "ALTER USER zima WITH PASSWORD 'password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE zimalab TO zima;"
```

### 3. Start the Pi backend

```bash
cd rpi
cp .env.example .env        # edit DATABASE_URL and SERIAL_PORT as needed
uv sync
uv run alembic upgrade head
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### 4. Open the dashboard

On the local monitor, navigate to `http://localhost:8000` (production build served by FastAPI) or run the dev server:

```bash
cd frontend
npm install
npm run dev                 # opens http://localhost:5173, proxies API to :8000
```

## Data Export / ML

```bash
cd rpi
uv run python -m ml.export --start 2026-01-01 --out ../data/exports/dataset.parquet
```

The exported Parquet file has a `DatetimeIndex` and is ready for pandas, scikit-learn, or Prophet.
