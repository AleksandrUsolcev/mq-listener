import aio_pika
import aio_pika.abc
from aio_pika import DeliveryMode

from config import settings


class BrokerConnectionManager:
    amqp_url = settings.get_amqp_url

    def __init__(self):
        self.connection = None

    async def __aenter__(self):
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.connection is not None:
            await self.connection.close()


async def publish_message(
    connection: BrokerConnectionManager,
    routing_key: str,
    message: str
):
    channel: aio_pika.abc.AbstractChannel = await connection.channel()
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=message.encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
        ),
        routing_key=routing_key
    )


async def send_message(message: str, routing_key: str):
    async with BrokerConnectionManager() as manager:
        await publish_message(manager.connection, routing_key, message)
