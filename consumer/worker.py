import asyncio

import aio_pika
import aio_pika.abc
import websockets
from websockets.exceptions import ConnectionClosedError

from internal.logging import logger


class Worker:

    def __init__(
        self,
        amqp_url: str,
        ws_url: str,
        queue_name: str,
        worker_func: callable,
        timeout: int = 5
    ):
        self.amqp_url = amqp_url
        self.ws_url = ws_url
        self.queue_name = queue_name
        self.worker_func = worker_func
        self.timeout = timeout

        self.loop = asyncio.get_event_loop()
        self.ws = None

    async def _websocket_connection(self):
        while True:
            try:
                self.ws = await websockets.connect(self.ws_url)
                logger.info(f'WebSocket connection: {self.ws_url}')
                return
            except (ConnectionClosedError, ConnectionRefusedError):
                logger.error(
                    'WebSocket connection closed unexpectedly. '
                    'Reconnecting...'
                )
                await asyncio.sleep(self.timeout)

    async def _process_message(self, message):
        text = message.body.decode()
        data = await self.worker_func(text)
        await self.ws.send(data)
        async with message.process():
            if self.queue_name in message.body.decode():
                return True

    async def _queue_processing(self, queue):
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await self._process_message(message)

    async def _consume(self):
        connection = await aio_pika.connect_robust(
            self.amqp_url,
            loop=self.loop
        )
        async with connection:
            channel: aio_pika.abc.AbstractChannel = await connection.channel()
            queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
                self.queue_name,
                durable=True,
            )
            await self._websocket_connection()
            await self._queue_processing(queue)

    async def run(self):
        while True:
            try:
                await self._consume()
            except Exception as e:
                logger.error(e)
                await asyncio.sleep(self.timeout)
