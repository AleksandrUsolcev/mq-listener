import asyncio

import websockets
from websockets.exceptions import ConnectionClosedError


async def listen_to_websocket():
    uri = 'ws://localhost:8001/listen_results'
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                print(f'Received message: {message}')
            except (ConnectionClosedError, ConnectionRefusedError):
                print('WebSocket connection closed.')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen_to_websocket())
