import asyncpg
from config import settings


class DBConnection:
    def __init__(self, db_url: str) -> None:
        self._db_url = db_url

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(
            dsn=self._db_url,
            min_size=1,
            max_size=15,
            max_queries=50000,
            max_inactive_connection_lifetime=300.0,
        )

    @property
    def pool(self) -> asyncpg.Pool:
        return self._pool

    async def disconnect(self) -> None:
        await self._pool.close()


database = DBConnection(settings.DATABASE_URL)
