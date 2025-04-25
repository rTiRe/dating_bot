from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from src.handlers.router import router, default_router
from src.templates import render
from src.handlers.menu import menu


@router.message(CommandStart())
@default_router.message()
async def start_handler(message: types.Message, state: FSMContext) -> None | types.Message:
    if not message.from_user:
        return None
    bot_message = await message.answer(
        await render('start'),
    )
    await state.set_state(default_state)
    await menu(message, state)
    return bot_message
