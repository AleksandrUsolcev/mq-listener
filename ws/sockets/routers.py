from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from sockets.managers import ConnectionManager

router = APIRouter()

manager = ConnectionManager()


@router.websocket('/listen_results')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
