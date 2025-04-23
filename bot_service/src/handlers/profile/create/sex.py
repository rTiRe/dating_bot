from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.handlers.profile.create.router import router
from src.templates import render
from src.states import ProfileCreationStates

@router.message(ProfileCreationStates.age, F.text)
async def sex(message: types.Message, state: FSMContext) -> types.Message:
    try:
        user_age = int(message.text)
    except ValueError:
        return await message.answer(
            text='Возраст должен быть числом. Попробуй еще раз',
        )
    if not 6 < user_age < 100:
        return await message.answer(
            text='Возраст должен быть не меньше 7 и не больше 99. Попробуй еще раз',
        )
    await state.update_data(age=user_age)
    bot_message = await message.answer(
        await render('profile/create/3_sex'),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Я парень'),
                    KeyboardButton(text='Я девушка'),
                ],
            ],
            is_persistent=True,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )
    await state.set_state(ProfileCreationStates.sex)
    return bot_message


@router.message(ProfileCreationStates.age)
async def sex_error(message: types.Message) -> types.Message:
    return await message.answer('Мне нужно знать твой возраст')
