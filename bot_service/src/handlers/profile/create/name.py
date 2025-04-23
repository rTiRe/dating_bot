from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.handlers.profile.create.router import router
from src.templates import render
from src.states import ProfileCreationStates

@router.message(F.text.lower() == 'создать анкету')
async def name(message: types.Message, state: FSMContext) -> types.Message:
    bot_message = await message.answer(
        await render('profile/create/1_name'),
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
