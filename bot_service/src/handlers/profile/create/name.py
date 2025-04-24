from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.handlers.profile.create.router import router
from src.templates import render
from src.states import ProfileCreationStates, ProfileUpdateStates, MainStates

@router.message(MainStates.menu, F.text.lower() == '4')
async def name(message: types.Message, state: FSMContext) -> types.Message:
    is_creation = await state.get_state() != MainStates.menu
    bot_message = await message.answer(
        await render(
            'profile/create/1_name',
            first_meet=is_creation,
        ),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Взять из профиля')],
            ],
            is_persistent=True,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder='Меня зовут...',
        )
    )
    if is_creation:
        await state.set_state(ProfileCreationStates.name)
    else:
        await state.set_state(ProfileUpdateStates.name)
    return bot_message
