import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from config import settings, logger
from src.bot import setup_dispatcher, setup_bot
from src.handlers import router


logger = logger(__name__)


async def setup_app() -> tuple[Dispatcher, Bot]:
    dispatcher = Dispatcher(storage=None)
    setup_dispatcher(dispatcher)
    dispatcher.include_router(router)
    # dispatcher.message.outer_middleware(ThrottlingMiddleware(limit=2))
    # dispatcher.message.outer_middleware(StartMiddleware())
    # dispatcher.message.outer_middleware(CheckSubscriptionMiddleware())
    # dispatcher.callback_query.outer_middleware(CheckSubscriptionMiddleware())
    # dispatcher.message.middleware(StateMiddleware())
    # dispatcher.callback_query.middleware(StateMiddleware())
    default_properties = DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    )
    bot = Bot(token=settings.BOT_TOKEN, default=default_properties)
    await bot.delete_webhook()
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Перезапустить бота')
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )
    setup_bot(bot)
    # asyncio.create_task(setup_rabbit())
    return (dispatcher, bot)


async def start_polling() -> None:
    dispatcher, bot = await setup_app()
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_polling())