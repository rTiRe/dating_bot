from contextlib import asynccontextmanager
from typing import AsyncGenerator

from asyncpg.exceptions import UniqueViolationError
import uvicorn
from fastapi import FastAPI

from config import logger
from src.exceptions import DeleteAllRowsException
from src.storage import database
from src.specifications import EqualsSpecification
from src.repositories import AccountRepository
from src.schemas import CreateAccountSchema


logger = logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await database.connect()
    async with database.pool.acquire() as connection:
        try:
            await AccountRepository.create(connection, CreateAccountSchema(telegram_id=1))
        except UniqueViolationError as e:
            logger.error(e)
        logger.info(
            await AccountRepository.get(connection, EqualsSpecification('telegram_id', 1)),
        )
        try:
            await AccountRepository.delete(connection)
        except DeleteAllRowsException as e:
            logger.error(e)
    yield
    await database.disconnect()


def create_app() -> FastAPI:
    return FastAPI(docs_url='/swagger', lifespan=lifespan)


if __name__ == '__main__':
    uvicorn.run(
        'src.__main__:create_app',
        factory=True,
        host='127.0.0.1',
        port=8001,
        workers=1,
        access_log=False,
    )
