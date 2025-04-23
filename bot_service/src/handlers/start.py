from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from src.api.grpc.connections import accounts_connection
from src.handlers.router import router
from src.templates import render
from src.handlers.profile.create.name import name


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext) -> None | types.Message:
    if not message.from_user:
        return None
    await accounts_connection.get_or_create(message.from_user.id, message.from_user.username)
    bot_message = await message.answer(
        await render('start'),
    )
    await state.set_state(default_state)
    await name(message, state)
    return bot_message
