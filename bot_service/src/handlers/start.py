from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.api.grpc.connections import accounts_connection
from src.handlers.router import router


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext) -> None | types.Message:
    if not message.from_user:
        return None
    account = await accounts_connection.get_or_create(message.from_user.id, message.from_user.username)
    return await message.answer(f'Hello, {account.id}')
