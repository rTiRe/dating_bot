"""Main module."""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from config import logger, settings
from src.bot import setup_bot, setup_dispatcher
from src.handlers import router
from src.storage.rabbit import channel_pool

logger = logger(__name__)


async def setup_rabbit() -> None:
    """Set up RabbitMQ."""
    async with channel_pool.acquire() as channel:  # noqa: F841
        ...  # noqa: WPS428


async def setup_app() -> tuple[Dispatcher, Bot]:
    """Set up bot app.

    Returns:
        tuple[Dispatcher, Bot]: bot data.
    """
    dispatcher = Dispatcher(storage=None)
    setup_dispatcher(dispatcher)
    dispatcher.include_router(router)
    default_properties = DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    )
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), default=default_properties)
    await bot.delete_webhook()
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Перезапустить бота'),
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )
    setup_bot(bot)
    asyncio.create_task(setup_rabbit())
    return (dispatcher, bot)


async def start_polling() -> None:
    """Start bot polling."""
    dispatcher, bot = await setup_app()
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_polling())
