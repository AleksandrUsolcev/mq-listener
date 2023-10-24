import asyncio

from internal.config import settings
from services.text import reverse_text
from worker import Worker


async def main():
    consumer = Worker(
        amqp_url=settings.get_amqp_url,
        ws_url=settings.get_ws_url,
        queue_name=settings.RABBITMQ_QUEUE_NAME,
        worker_func=reverse_text,
        timeout=settings.CONSUMER_RECONNECT_TIMEOUT,
    )
    await consumer.run()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
