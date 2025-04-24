from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import ProfileCreationStates, MainStates

@router.message(MainStates.menu, F.text.lower() == '4')
async def name(message: types.Message, state: FSMContext) -> types.Message:
    bot_message = await message.answer(
        await render(
            'profile/create/1_name',
            first_meet=(await state.get_data()).get('profile_id') is None,
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
    await state.set_state(ProfileCreationStates.name)
    return bot_message
