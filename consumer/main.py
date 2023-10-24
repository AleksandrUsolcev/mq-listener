import asyncio

from internal.config import settings
from internal.logging import logger
from worker import consume


async def main():
    while True:
        try:
            await consume(
                loop=loop,
                amqp_url=settings.get_amqp_url,
                ws_url=settings.get_ws_url,
                queue_name=settings.RABBITMQ_QUEUE_NAME,
            )
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(settings.CONSUMER_RECONNECT_TIMEOUT)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
