#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="zimalab.service"
SERVICE_TEMPLATE="$ROOT/deploy/zimalab.service.in"
ENV_FILE="$ROOT/rpi/.env"

if [[ $EUID -eq 0 ]]; then
  echo "Run this script as the account that owns the Zima Lab checkout, not as root." >&2
  exit 1
fi

for command in npm uv sudo systemctl sed; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Required command not found: $command" >&2
    exit 1
  fi
done

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE. Copy rpi/.env.example to rpi/.env and configure it first." >&2
  exit 1
fi

UV="$(command -v uv)"
RUN_USER="$(id -un)"
UNIT_TMP="$(mktemp)"
trap 'rm -f "$UNIT_TMP"' EXIT

echo "Installing frontend dependencies and building the production dashboard..."
npm --prefix "$ROOT/frontend" ci
npm --prefix "$ROOT/frontend" run build

echo "Installing backend dependencies and applying database migrations..."
(
  cd "$ROOT/rpi"
  uv sync
  uv run alembic upgrade head
)

# The replacement values are filesystem paths/usernames and cannot contain "|".
sed \
  -e "s|@USER@|$RUN_USER|g" \
  -e "s|@ROOT@|$ROOT|g" \
  -e "s|@UV@|$UV|g" \
  "$SERVICE_TEMPLATE" > "$UNIT_TMP"

echo "Installing and restarting $SERVICE_NAME..."
sudo install -m 0644 "$UNIT_TMP" "/etc/systemd/system/$SERVICE_NAME"
sudo systemctl daemon-reload
sudo systemctl enable --now "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo
sudo systemctl --no-pager --full status "$SERVICE_NAME"
echo
echo "Deployment complete: http://$(hostname -I | awk '{print $1}'):8000"
echo "Follow logs with: journalctl -u $SERVICE_NAME -f"
