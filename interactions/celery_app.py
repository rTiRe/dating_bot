from celery import Celery

app = Celery(
    'interactions',
    broker='amqp://admin:admin@rabbitmq:5672//',
    include=['tasks']    # ← ключевой момент
)
app.conf.beat_schedule = {
    'mutual-every-10s': {
        'task': 'tasks.run_mutual_worker',
        'schedule': 10.0
    }
}
