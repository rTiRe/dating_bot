import asyncio
import json
from aio_pika import connect_robust, Message, Queue, DeliveryMode, ExchangeType # type: ignore
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractQueue # type: ignore
from config import *

async def send_message(connection: AbstractConnection, interaction_type: InteractionType, data: dict):
    channel: AbstractChannel = await connection.channel()

    exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        type=ExchangeType.FANOUT,
        durable=True,
        passive=True,
    )

    queue: AbstractQueue = await channel.declare_queue(QUEUE_NAME, durable=True)

    await queue.bind(exchange, routing_key='')
    # for i in range(50):
    data[INTERACTION_TYPE_FIELD] = interaction_type.value
        # data[LIKER_ID_FIELD] = i
        # data[LIKED_ID_FIELD] = 50 - i
    message = Message(
            body=json.dumps(data).encode(),
            delivery_mode=DeliveryMode.PERSISTENT
        )
    await exchange.publish(message, routing_key='')
    print(f"Sent message: {data}")



async def main():
    try:
        connection = await connect_robust(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            login=RABBITMQ_USER,
            password=RABBITMQ_PASSWORD
            )
        await send_message(connection, InteractionType.LIKE, {LIKER_ID_FIELD: 'abcd', LIKED_ID_FIELD: 'b1d'})
        await send_message(connection, InteractionType.LIKE, {LIKER_ID_FIELD: 'b1d', LIKED_ID_FIELD: 'abcd'})
        # await send_message(connection, InteractionType.LIKE, {LIKER_ID_FIELD: 'b1d', LIKED_ID_FIELD: 'd1b'})
        # await send_message(connection, InteractionType.LIKE, {LIKER_ID_FIELD: 'd1b', LIKED_ID_FIELD: 'b1d'})

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            await connection.close()


if __name__ == "__main__":
    asyncio.run(main())

