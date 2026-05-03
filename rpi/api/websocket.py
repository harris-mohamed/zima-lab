from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from broadcast.hub import hub

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/sensors")
async def sensor_websocket(ws: WebSocket):
    await hub.connect(ws)
    try:
        while True:
            # Keep the connection alive; all data is server-pushed via hub.broadcast().
            await ws.receive_text()
    except WebSocketDisconnect:
        hub.disconnect(ws)
