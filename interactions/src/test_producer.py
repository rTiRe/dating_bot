import asyncio
import json
from aio_pika import connect_robust, Message, Queue, DeliveryMode
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractQueue
from interactions_service import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD, LIKE_QUEUE, DISLIKE_QUEUE, LIKER_ID_FIELD, LIKED_ID_FIELD, DISLIKER_ID_FIELD, DISLIKED_ID_FIELD


async def send_message(connection: AbstractConnection, queue_name: str, data: dict):
    channel: AbstractChannel = await connection.channel()
    queue: AbstractQueue = await channel.declare_queue(queue_name, durable=True)

    message = Message(
        body=json.dumps(data).encode(),
        delivery_mode=DeliveryMode.PERSISTENT
    )

    await channel.default_exchange.publish(message, routing_key=queue_name)
    print(f"Sent message to {queue_name}: {data}")


async def main():
    try:
        connection = await connect_robust(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            login=RABBITMQ_USER,
            password=RABBITMQ_PASSWORD
            )
        await send_message(connection, LIKE_QUEUE, {LIKER_ID_FIELD: 1, LIKED_ID_FIELD: 2})
        await send_message(connection, DISLIKE_QUEUE, {DISLIKER_ID_FIELD: 1, DISLIKED_ID_FIELD: 2})
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            await connection.close()


if __name__ == "__main__":
    asyncio.run(main())

