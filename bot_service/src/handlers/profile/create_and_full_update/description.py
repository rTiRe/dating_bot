from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import ProfileCreationStates

@router.message(ProfileCreationStates.sex_preferences, F.text.lower().in_(['парни', 'девушки', 'все равно']))
async def description(message: types.Message, state: FSMContext) -> types.Message:
    preference_text = message.text.lower()
    if preference_text == 'парни':
        sex_preference = 'M'
    elif preference_text == 'девушки':
        sex_preference = 'F'
    else:
        sex_preference = 'N'
        await state.update_data(sex_preference=sex_preference)
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


@router.message(ProfileCreationStates.sex_preferences)
async def description_error(message: types.Message) -> types.Message:
    return await message.answer('Я тебя не понял. Используй кнопки на клавиатуре')
