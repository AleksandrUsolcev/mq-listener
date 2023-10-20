import asyncio
import json
import logging
from typing import Dict

import aio_pika
import aio_pika.abc
import websockets
from websockets.exceptions import ConnectionClosedError

from config import settings

logging.basicConfig(
    format='%(asctime)s: %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


async def reverse_text(text: str) -> Dict[str, str]:
    reversed_text = text[::-1]
    return json.dumps({'reversed_text': reversed_text}, ensure_ascii=False)


async def send_result_to_websocket(data: Dict[str, str], ws):
    await ws.send(data)


async def consume_and_send_to_websocket(queue, ws):
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                text = message.body.decode()
                data = await reverse_text(text)
                await send_result_to_websocket(data, ws)
                if queue.name in message.body.decode():
                    break


async def consume_and_reconnect(loop):
    while True:
        connection = await aio_pika.connect_robust(
            settings.get_amqp_url,
            loop=loop
        )
        async with connection:
            queue_name = settings.RABBITMQ_QUEUE_NAME
            channel: aio_pika.abc.AbstractChannel = await connection.channel()
            queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
                queue_name,
                durable=True,
            )

            async with websockets.connect(settings.get_ws_url) as ws:
                logger.info(f'WebSocket connection: {settings.get_ws_url}')
                await consume_and_send_to_websocket(queue, ws)


async def main():
    while True:
        try:
            await consume_and_reconnect(loop)
        except (ConnectionClosedError, ConnectionRefusedError):
            logger.error(
                'WebSocket connection closed unexpectedly. Reconnecting...'
            )
            await asyncio.sleep(5)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
