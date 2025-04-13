"""RabbitMQ Configuration Module."""

import aio_pika
import msgpack
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from config.settings import settings


async def get_connection() -> AbstractRobustConnection:
    """Get RabbitMQ conncetion.

    Returns:
        AbstractRobustConnection: RabbitMQ connection
    """
    return await aio_pika.connect_robust(settings.RABBITMQ_URL)


connection_pool: Pool = Pool(get_connection, max_size=2)


async def get_channel() -> aio_pika.Channel:
    """Get channel from connection pool.

    Returns:
        aio_pika.Channel: connection channel
    """
    async with connection_pool.acquire() as connection:
        return await connection.channel()


channel_pool: Pool = Pool(get_channel, max_size=10)


async def publish_message(routing_key: str, message: dict, **kwargs) -> None:
    """Publish message to routing key.

    Args:
        routing_key (str): queue routing key
        message (dict): message for publish
        kwargs: message parameters
    """
    async with channel_pool.acquire() as channel:
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=msgpack.packb(message),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                **kwargs,
            ),
            routing_key=routing_key,
        )
