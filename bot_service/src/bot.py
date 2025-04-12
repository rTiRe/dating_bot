from aiogram import Bot, Dispatcher


bot: Bot
dp: Dispatcher


def setup_bot(_bot: Bot) -> None:
    global bot
    bot = _bot


def get_bot() -> Bot:
    global bot
    return bot


def setup_dispatcher(_dp: Dispatcher) -> None:
    global dp
    dp = _dp


def get_dispatcher() -> Dispatcher:
    global dp
    return dp
