import dataclasses
import json
import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self._connections: set[WebSocket] = set()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._connections.add(ws)
        logger.debug("WebSocket connected; total=%d", len(self._connections))

    def disconnect(self, ws: WebSocket) -> None:
        self._connections.discard(ws)
        logger.debug("WebSocket disconnected; total=%d", len(self._connections))

    async def broadcast(self, data: Any) -> None:
        if not self._connections:
            return
        if dataclasses.is_dataclass(data):
            payload = json.dumps(dataclasses.asdict(data))
        else:
            payload = json.dumps(data)

        dead: set[WebSocket] = set()
        for ws in self._connections:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.add(ws)

        self._connections -= dead


hub = ConnectionManager()
