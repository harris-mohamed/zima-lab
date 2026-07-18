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

### 4. Start both backend and frontend for development

From the repo root:

```bash
bash scripts/dev.sh
```

The script starts FastAPI on `http://localhost:8000` and Vite on `http://localhost:5173`, then shuts both down when you press Ctrl+C.

You can override the bind host/ports:

```bash
BACKEND_PORT=8001 FRONTEND_PORT=5174 bash scripts/dev.sh
```

### 5. Open the dashboard

On the local monitor, navigate to `http://localhost:8000` (production build served by FastAPI) or run the dev server:

```bash
cd frontend
npm install
npm run dev                 # opens http://localhost:5173, proxies API to :8000
```

## Deploy on the Raspberry Pi

The production deployment runs the API and built dashboard as one systemd
service. From the repository root on the Pi:

```bash
chmod +x deploy.sh
./deploy.sh
```

The script installs dependencies, builds the frontend, applies database
migrations, installs `zimalab.service`, and restarts it. It deploys the current
checkout; pull or copy the desired code before running it.

Useful service commands:

```bash
sudo systemctl status zimalab
sudo systemctl restart zimalab
journalctl -u zimalab -f
journalctl -u zimalab --since today
```

The service starts automatically at boot and restarts after failures. The
dashboard is available at `http://10.0.0.123:8000`.

## Data Export / ML

```bash
cd rpi
uv run python -m ml.export --start 2026-01-01 --out ../data/exports/dataset.parquet
```

The exported Parquet file has a `DatetimeIndex` and is ready for pandas, scikit-learn, or Prophet.
