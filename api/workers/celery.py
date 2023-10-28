import time

from asgiref.sync import async_to_sync
from celery import Celery

from internal.config import settings
from internal.logging import logger
from services.mq_publisher import send_message

app = Celery(
    'celery_worker',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0',
)


@async_to_sync
async def send_message_sync(message, routing_key):
    await send_message(message, routing_key)


@app.task
def send_message_to_queue(message, routing_key):
    while True:
        try:
            send_message_sync(message, routing_key)
            break
        except Exception:
            logger.info(
                f'Retrying in {settings.RABBITMQ_RECONNECT_TIMEOUT} seconds.'
            )
            time.sleep(settings.RABBITMQ_RECONNECT_TIMEOUT)
