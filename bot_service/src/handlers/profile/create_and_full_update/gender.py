from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import lazy_gettext as _

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import ProfileCreationStates

@router.message(ProfileCreationStates.age, F.text)
async def gender(message: types.Message, state: FSMContext) -> types.Message:
    try:
        user_age = int(message.text)
    except ValueError:
        return await message.answer(
            text=str(_('Возраст должен быть числом. Попробуй еще раз')),
        )
    if not 6 < user_age < 100:
        return await message.answer(
            text=str(_('Возраст должен быть не меньше 7 и не больше 99. Попробуй еще раз')),
        )
    await state.update_data(age=user_age)
    bot_message = await message.answer(
        await render('profile/create/3_gender', language_code=message.from_user.language_code),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=str(_('Я парень'))),
                    KeyboardButton(text=str(_('Я девушка'))),
                ],
            ],
            is_persistent=True,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )
    await state.set_state(ProfileCreationStates.gender)
    return bot_message


@router.message(ProfileCreationStates.age)
async def gender_error(message: types.Message) -> types.Message:
    return await message.answer(str(_('Мне нужно знать твой возраст')))
