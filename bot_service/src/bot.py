"""Module for setup bot and dispatcher instances."""

from aiogram import Bot, Dispatcher

bot: Bot
dp: Dispatcher


def setup_bot(_bot: Bot) -> None:
    """Set bot globally.

    Args:
        _bot (Bot): bot instance
    """
    global bot
    bot = _bot


def get_bot() -> Bot:
    """Get bot instance.

    Returns:
        Bot: bot instance
    """
    global bot
    return bot


def setup_dispatcher(_dp: Dispatcher) -> None:
    """Set dispatcher globally.

    Args:
        _dp (Dispatcher): dispatcher instance
    """
    global dp
    dp = _dp


def get_dispatcher() -> Dispatcher:
    """Get dispatcher instance.

    Returns:
        Dispatcher: dispatcer instance
    """
    global dp
    return dp
