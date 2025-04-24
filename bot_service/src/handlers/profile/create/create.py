from aiogram import F, types
from aiogram.fsm.context import FSMContext

from src.handlers.profile.create.router import router
from src.states import ProfileCreationStates
from src.handlers.menu import menu

@router.message(ProfileCreationStates.description, F.text)
async def create(
    message: types.Message,
    state: FSMContext,
) -> tuple[types.Message, types.Message, types.Message] | types.Message:
    if message.text.lower() == 'пропустить':
        description = ''
    elif len(message.text) < 30:
        return await message.answer('Напиши хоть несколько слов о себе')
    else:
        description = message.text
    await state.update_data(description=description)
    data = await state.get_data()
    # CREATE
    return await menu(message, state)


@router.message(ProfileCreationStates.description)
async def check_error(message: types.Message) -> types.Message:
    return await message.answer('Я тебя не понял. Пришли мне текст')
