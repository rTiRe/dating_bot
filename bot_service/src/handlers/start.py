from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from src.handlers.router import router


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext) -> types.Message:
    return await message.answer('hello')
