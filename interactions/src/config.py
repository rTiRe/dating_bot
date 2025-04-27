import os
from enum import Enum

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'admin')

class InteractionType(Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'

    @classmethod
    def from_string(cls, value: str) -> 'InteractionType':
        if value == 'like':
            return cls.LIKE
        elif value == 'dislike':
            return cls.DISLIKE
        else:
            raise ValueError(f"Invalid interaction type: {value}")

# Queue names
QUEUE_NAME = 'interactions_queue'
EXCHANGE_NAME = 'interactions_exchange'

LIKER_ID_FIELD = 'liker_id'
LIKED_ID_FIELD = 'liked_id'

INTERACTION_TYPE_FIELD = 'interaction_type'
