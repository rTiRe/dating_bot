import asyncio
import json
import os
from typing import Dict, Any
from aio_pika import connect_robust, Message, Queue
from aio_pika.abc import AbstractChannel, AbstractConnection

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'admin')

# Queue names
LIKE_QUEUE = 'likes'
DISLIKE_QUEUE = 'dislikes'



class InteractionsService:
    def __init__(self):
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.like_queue: AbstractQueue | None = None
        self.dislike_queue: AbstractQueue | None = None

    async def setup(self):
        self.connection = await connect_robust




# import asyncio
# import json
# import os
# from typing import Dict, Any
# from aio_pika import connect_robust, Message, Queue
# from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue

# # RabbitMQ connection parameters
# RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
# RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
# RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
# RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'admin')

# # Queue names
# LIKE_QUEUE = 'likes'
# DISLIKE_QUEUE = 'dislikes'

# class InteractionsService:
#     def __init__(self):
#         self.connection: AbstractConnection | None = None
#         self.channel: AbstractChannel | None = None
#         self.like_queue: AbstractQueue | None = None
#         self.dislike_queue: AbstractQueue | None = None

#     async def setup_rabbitmq(self):
#         """Setup RabbitMQ connection and queues"""
#         self.connection = await connect_robust(
#             host=RABBITMQ_HOST,
#             port=RABBITMQ_PORT,
#             login=RABBITMQ_USER,
#             password=RABBITMQ_PASSWORD
#         )

#         self.channel = await self.connection.channel()

#         # Declare queues
#         self.like_queue = await self.channel.declare_queue(
#             LIKE_QUEUE,
#             durable=True
#         )
#         self.dislike_queue = await self.channel.declare_queue(
#             DISLIKE_QUEUE,
#             durable=True
#         )

#     async def process_like(self, message: Message):
#         """Process like interaction"""
#         async with message.process():
#             try:
#                 data = json.loads(message.body.decode())
#                 # TODO: Add database integration here
#                 print(f"Received like: {data}")
#             except Exception as e:
#                 print(f"Error processing like: {e}")

#     async def process_dislike(self, message: Message):
#         """Process dislike interaction"""
#         async with message.process():
#             try:
#                 data = json.loads(message.body.decode())
#                 # TODO: Add database integration here
#                 print(f"Received dislike: {data}")
#             except Exception as e:
#                 print(f"Error processing dislike: {e}")

#     async def start_consuming(self):
#         """Start consuming messages from queues"""
#         await self.like_queue.consume(self.process_like)
#         await self.dislike_queue.consume(self.process_dislike)
#         print('Started consuming messages...')

#     async def run(self):
#         """Run the service"""
#         try:
#             await self.setup_rabbitmq()
#             await self.start_consuming()

#             # Keep the service running
#             while True:
#                 await asyncio.sleep(1)

#         except Exception as e:
#             print(f"Error in run: {e}")
#         finally:
#             if self.connection:
#                 await self.connection.close()

# async def main():
#     service = InteractionsService()
#     await service.run()

# if __name__ == "__main__":
#     asyncio.run(main())
