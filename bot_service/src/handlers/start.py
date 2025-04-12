from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from src.handlers.router import router
from src.api.grpc.connections import accounts_connection


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext) -> types.Message:
    account = await accounts_connection.get_or_create(message.from_user.id, message.from_user.username)
    return await message.answer(f'Hello, {account.id}')
