# Zima Lab

Automated hydroponics monitoring system. Arduino MEGA reads analog sensors and sends JSON over serial to a Raspberry Pi, which stores data in PostgreSQL and serves a React dashboard.

## Architecture

```
[Arduino MEGA] ──serial──┐
[Kasa plugs]   ──network─┼──► rpi/
[Camera]       ──USB──────┘     ├─ serial_reader/  →  db/      →  PostgreSQL
                                ├─ kasa/           →  influx/  →  InfluxDB
                                ├─ camera/            (MJPEG streams)
                                └─ api/               (FastAPI :8000)
                                         │ HTTP + WebSocket
                                         ▼
                                    frontend/  (React/Vite :5173)
```

## Directory Layout

```
arduino/   C++ sensor sketch for Arduino MEGA
rpi/       Python backend (FastAPI, SQLAlchemy, serial reader)
frontend/  React + Vite dashboard
data/      gitignored runtime data (DB exports)
```

## Arduino

- Sketch: `arduino/hydroponics_sensors/hydroponics_sensors.ino`
- Pin assignments and calibration constants: `arduino/hydroponics_sensors/config.h`
- Sensor drivers in `arduino/hydroponics_sensors/sensors/` (one `.h/.cpp` pair per sensor)
- Required libraries (install via Arduino Library Manager): OneWire, DallasTemperature, DHT sensor library (Adafruit)
- Serial output: newline-delimited JSON at 115200 baud, e.g.:
  `{"ts":1234,"ph":6.2,"tds":840,"water_temp":22.1,"air_temp":24.5,"humidity":68.2,"water_level_cm":18.4}`
- Sensor error/disconnected state is reported as `-1.0`; the Pi converts these to `null`

## RPi Backend

**Package manager:** `uv` — use `uv add <pkg>` to add dependencies, `uv sync` to install, `uv run <cmd>` to execute.

```bash
cd rpi
cp .env.example .env        # set DATABASE_URL, SERIAL_PORT
uv sync
uv run alembic upgrade head
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**Key modules:**

| Path | Purpose |
|---|---|
| `config/settings.py` | Pydantic `BaseSettings` — all config from `.env` |
| `serial_reader/parser.py` | JSON line → `SensorReading` dataclass |
| `serial_reader/reader.py` | asyncio task: serial → DB + WebSocket broadcast |
| `db/models.py` | SQLAlchemy ORM model (`SensorReading` table) |
| `db/database.py` | Async engine + `AsyncSessionLocal` session factory |
| `db/writer.py` | `write_sensor_reading(session, reading)` |
| `db/queries.py` | `get_latest`, `get_history`, `export_dataframe` |
| `broadcast/hub.py` | WebSocket `ConnectionManager` — fan-out to all clients |
| `api/main.py` | FastAPI app factory with `lifespan` — wires everything |
| `api/deps.py` | `get_session()` FastAPI dependency |
| `camera/picam_stream.py` | picamera2 MJPEG generator |
| `camera/usb_cam_stream.py` | OpenCV USB webcam MJPEG generator |
| `ml/export.py` | CLI: dump DB range to CSV/Parquet for ML |

**Running tests:**
```bash
cd rpi
uv run pytest
```
Tests hit a real PostgreSQL instance at `DATABASE_URL` with `_test` suffix DB.

**Adding a new sensor:**
1. Add column to `db/models.py` (`SensorReading` class)
2. Run `uv run alembic revision --autogenerate -m "add <sensor>"` then `uv run alembic upgrade head`
3. Add field to `SensorReading` dataclass in `serial_reader/parser.py`
4. Update `db/writer.py` to map the new field

## Frontend

```bash
cd frontend
npm install
npm run dev     # dev server at :5173, proxies /api/* and /ws/* to :8000
npm run build   # outputs to frontend/dist/ — served by FastAPI in production
```

**Key files:**

| Path | Purpose |
|---|---|
| `src/types/sensors.ts` | `SensorReading` TypeScript interface |
| `src/hooks/useSensorWebSocket.ts` | WS connection with exponential backoff reconnect |
| `src/hooks/useSensorHistory.ts` | Fetches historical readings on mount |
| `src/components/SensorCard.tsx` | Single reading display with optional warn threshold |
| `src/components/SensorChart.tsx` | Recharts rolling time-series chart |
| `src/components/CameraFeed.tsx` | MJPEG `<img>` with auto-reload on error |
| `vite.config.ts` | Proxies `/api` and `/ws` to `localhost:8000` |

## Data Flow

```
Arduino MEGA
  → Serial JSON @ 115200 baud → /dev/ttyUSB0

rpi/serial_reader/reader.py  (asyncio task)
  → parser.py → SensorReading dataclass
  → db/writer.py → PostgreSQL INSERT
  → broadcast/hub.py → WebSocket fan-out

Frontend
  useSensorWebSocket ← WS /ws/sensors   (live, ~1/s)
  useSensorHistory   ← GET /api/sensors/history (seed on mount)
  CameraFeed         ← GET /api/cameras/picam   (MJPEG)
```

## Environment Variables (`rpi/.env`)

| Variable | Default | Description |
|---|---|---|
| `SERIAL_PORT` | `/dev/ttyUSB0` | Arduino serial device |
| `SERIAL_BAUD` | `115200` | Serial baud rate |
| `DATABASE_URL` | `postgresql+asyncpg://zima:password@localhost:5432/zimalab` | Async SQLAlchemy URL |
| `API_HOST` | `0.0.0.0` | FastAPI bind host |
| `API_PORT` | `8000` | FastAPI bind port |
| `USB_CAM_DEVICE` | `0` | OpenCV camera source — prefer a stable `/dev/v4l/by-id/...` symlink over a numeric index, since `/dev/videoN` assignment isn't stable across reboots/replugs |
