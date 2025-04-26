# Interactions Service

A microservice for handling likes and dislikes using RabbitMQ.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables (optional):
Create a `.env` file with the following variables:
```
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=admin
```

## Running the Service

```bash
python src/interactions_service.py
```

## Message Format

The service expects JSON messages in the following format:

```json
{
    "user_id": "123",
    "target_id": "456",
    "timestamp": "2024-03-20T12:00:00Z"
}
```

## Queues

- `likes` - Queue for like interactions
- `dislikes` - Queue for dislike interactions
