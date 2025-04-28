
import asyncio
import json
from aio_pika import connect_robust, Message, DeliveryMode, ExchangeType # type: ignore
from datetime import datetime

import clickhouse_connect # type: ignore

async def start_mutual_worker():

    ch = await clickhouse_connect.get_async_client(
        host="clickhouse_instance",
        port=8123,
        username="default",
        password="default",
    )

    rmq = await connect_robust(
        host='rabbitmq',
        port=5672,
        login='admin',
        password='admin',
    )
    channel = await rmq.channel()
    exchange = await channel.declare_exchange(
        "mutual_likes_exchange", ExchangeType.FANOUT, durable=True, passive=True
    )


    q = """
        SELECT liker1, liker2, event_time
        FROM dating.mutual_likes_log
        WHERE sent = 0
    """
    result = await ch.query(q)

    for liker1, liker2, event_time in result.result_set:
        payload = {
            "user1": liker1,
            "user2": liker2,
            "time": event_time.isoformat()
        }
        msg = Message(
            body=json.dumps(payload).encode(),
            delivery_mode=DeliveryMode.PERSISTENT
        )
        await exchange.publish(msg, routing_key="")
        await ch.command(
            f"ALTER TABLE dating.mutual_likes_log "
            f"UPDATE sent = 1 "
            f"WHERE liker1={liker1} AND liker2={liker2} "
        )



    await rmq.close()
    await ch.close()
