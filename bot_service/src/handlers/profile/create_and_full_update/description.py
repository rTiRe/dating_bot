from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import ProfileCreationStates

@router.message(ProfileCreationStates.interested_in, F.text.lower().in_(['парни', 'девушки', 'все равно']))
async def description(message: types.Message, state: FSMContext) -> types.Message:
    interested_in_text = message.text.lower()
    if interested_in_text == 'парни':
        interested_in = 'M'
    elif interested_in_text == 'девушки':
        interested_in = 'F'
    else:
        interested_in = 'N'
        await state.update_data(interested_in=interested_in)
    bot_message = await message.answer(
        await render(
            'profile/create/7_description',
            first_meet=(await state.get_data()).get('profile_id') is None,
        ),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Пропустить')],
            ],
            is_persistent=True,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder='Я - это ...',
        ),
    )
    await state.set_state(ProfileCreationStates.description)
    return bot_message


@router.message(ProfileCreationStates.interested_in)
async def description_error(message: types.Message) -> types.Message:
    return await message.answer('Я тебя не понял. Используй кнопки на клавиатуре')
