# interactions/tasks.py

import mutual
from celery_app import app

@app.task(name='tasks.run_mutual_worker')
def run_mutual_worker():
    import asyncio
    asyncio.run(mutual.start_mutual_worker())
