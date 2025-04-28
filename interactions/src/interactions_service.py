import asyncio
import json
from aio_pika import connect_robust, Message # type: ignore
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractQueue # type: ignore
from db import Database
from config import *




class InteractionsService:
    def __init__(self):
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.queue: AbstractQueue | None = None
        self.exit = False
        self.db = Database()

    async def setup(self):
        self.connection = await connect_robust(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            login=RABBITMQ_USER,
            password=RABBITMQ_PASSWORD
        )
        self.channel = await self.connection.channel() # type: ignore

        self.queue = await self.channel.declare_queue( # type: ignore
            QUEUE_NAME,
            durable=True
        )
        await self.db.setup()

    async def process_interaction(self, message: Message):
        async with message.process():
            try:
                data = json.loads(message.body.decode())
                interaction_type = InteractionType.from_string(data[INTERACTION_TYPE_FIELD])
                if interaction_type == InteractionType.LIKE:
                    await self.db.add_like(data[LIKER_ID_FIELD], data[LIKED_ID_FIELD])
                    print(f"Processed like: {data}")
                else:
                    await self.db.add_dislike(data[LIKER_ID_FIELD], data[LIKED_ID_FIELD])
                    print(f"Processed dislike: {data}")
            except Exception as e:
                print(f"Error processing interaction: {e}")

    async def start_consuming(self):
        await self.queue.consume(self.process_interaction) # type: ignore
        print('Started consuming messages...')


    async def run(self):
        """Run the service"""
        try:
            await self.setup()
            await self.start_consuming()

            while not self.exit:
                await asyncio.sleep(1)

        except Exception as e:
            print(f"Error in run: {e}")
        finally:
            if self.connection:
                await self.connection.close()



if __name__ == "__main__":
    service = InteractionsService()
    asyncio.run(service.run())

