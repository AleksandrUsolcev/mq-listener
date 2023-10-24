import aio_pika
import aio_pika.abc
import websockets
from websockets.exceptions import ConnectionClosedError

from internal.logging import logger
from services.text import reverse_text


async def queue_processing(queue, ws):
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                text = message.body.decode()
                data = await reverse_text(text)
                await ws.send(data)
                if queue.name in message.body.decode():
                    break


async def websocket_connection(queue, url):
    async with websockets.connect(url) as ws:
        try:
            logger.info(f'WebSocket connection: {url}')
            await queue_processing(queue, ws)
        except (ConnectionClosedError, ConnectionRefusedError):
            logger.error(
                'WebSocket connection closed unexpectedly. Reconnecting...'
            )


async def consume(loop, amqp_url, ws_url, queue_name):
    connection = await aio_pika.connect_robust(amqp_url, loop=loop)
    async with connection:
        channel: aio_pika.abc.AbstractChannel = await connection.channel()
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            durable=True,
        )
        await websocket_connection(queue, ws_url)
