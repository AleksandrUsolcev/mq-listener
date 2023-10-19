import asyncio
import json
from typing import Dict

import aio_pika
import aio_pika.abc
import websockets

from config import settings


async def reverse_text(text: str) -> Dict[str, str]:
    reversed_text = text[::-1]
    return json.dumps({'reversed_text': reversed_text}, ensure_ascii=False)


async def send_result_to_websocket(data: Dict[str, str]):
    async with websockets.connect(settings.get_ws_url) as ws:
        await ws.send(data)


async def main(loop):
    connection = await aio_pika.connect_robust(
        settings.get_amqp_url,
        loop=loop
    )

    async with connection:
        queue_name = settings.RABBITMQ_QUEUE_NAME
        channel: aio_pika.abc.AbstractChannel = await connection.channel()
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    text = message.body.decode()
                    data = await reverse_text(text)
                    await send_result_to_websocket(data)
                    if queue.name in message.body.decode():
                        break

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
