import asyncpg

from config import settings

MIN_POOL_SIZE = 1
MAX_POOL_SIZE = 15
MAX_POOL_QUERIES = 50000
MAX_POOL_INACTIVE_CONNECTION_LIFETIME = 300.0


class DBConnection:
    def __init__(self, db_url: str) -> None:
        self._db_url = db_url

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(
            dsn=self._db_url,
            min_size=MIN_POOL_SIZE,
            max_size=MAX_POOL_SIZE,
            max_queries=MAX_POOL_QUERIES,
            max_inactive_connection_lifetime=MAX_POOL_INACTIVE_CONNECTION_LIFETIME,
        )

    @property
    def pool(self) -> asyncpg.Pool:
        return self._pool

    async def disconnect(self) -> None:
        await self._pool.close()


database = DBConnection(settings.DATABASE_URL)