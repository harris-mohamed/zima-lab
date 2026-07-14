#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="${FRONTEND_HOST:-0.0.0.0}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  echo
  echo "Stopping Zima Lab dev servers..."
  if [[ -n "${FRONTEND_PID}" ]] && kill -0 "${FRONTEND_PID}" 2>/dev/null; then
    kill "${FRONTEND_PID}" 2>/dev/null || true
  fi
  if [[ -n "${BACKEND_PID}" ]] && kill -0 "${BACKEND_PID}" 2>/dev/null; then
    kill "${BACKEND_PID}" 2>/dev/null || true
  fi
  wait 2>/dev/null || true
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

trap cleanup EXIT INT TERM

require_command uv
require_command npm

echo "Starting Zima Lab dev servers..."
echo "Backend:  http://${BACKEND_HOST}:${BACKEND_PORT}"
echo "Frontend: http://${FRONTEND_HOST}:${FRONTEND_PORT}"
echo

(
  cd "${ROOT_DIR}/rpi"
  uv run uvicorn api.main:app --host "${BACKEND_HOST}" --port "${BACKEND_PORT}"
) &
BACKEND_PID=$!

(
  cd "${ROOT_DIR}/frontend"
  if [[ ! -d node_modules ]]; then
    echo "Installing frontend dependencies..."
    npm install
  fi
  npm run dev -- --host "${FRONTEND_HOST}" --port "${FRONTEND_PORT}"
) &
FRONTEND_PID=$!

wait -n "${BACKEND_PID}" "${FRONTEND_PID}"
