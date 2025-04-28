"""RabbitMQ Configuration Module."""
import json

import aio_pika
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


async def publish_message(exchange: str, routing_key: str, message: dict, **kwargs) -> None:
    """Publish message to routing key.

    Args:
        routing_key (str): queue routing key
        message (dict): message for publish
        kwargs: message parameters
    """
    async with channel_pool.acquire() as channel:
        channel: aio_pika.Channel
        await (await channel.get_exchange(exchange)).publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                **kwargs,
            ),
            routing_key=routing_key,
        )


async def publish_like(liker_id: str, liked_id: str) -> None:
    await publish_message(
        'interaction_exchange',
        'clickhouse_queue',
        {
            'liker_id': liker_id,
            'liked_id': liked_id,
            'interaction_type': 'like',
        }
    )


async def publish_dislike(liker_id: str, liked_id: str) -> None:
    await publish_message(
        'interaction_exchange',
        'clickhouse_queue',
        {
            'liker_id': liker_id,
            'liked_id': liked_id,
            'interaction_type': 'dislike',
        }
    )

