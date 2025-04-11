import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from config import logger
from src.storage import database
from src.api.grpc.services import AccountsService


logger = logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await database.connect()
    grpc_task = asyncio.create_task(AccountsService.serve())
    yield
    grpc_task.cancel()
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
