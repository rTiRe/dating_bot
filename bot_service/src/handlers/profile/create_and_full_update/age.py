from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import ProfileCreationStates

@router.message(ProfileCreationStates.name, F.text)
async def age(message: types.Message, state: FSMContext) -> types.Message:
    if message.text == 'Взять из профиля':
        user_name = message.from_user.first_name
    else:
        user_name = message.text
    if len(user_name) > 64:
        return await message.answer(
            text='Длина имени не может быть больше 64 символов. Попробуй еще раз',
        )
    await state.update_data(name=user_name)
    bot_message = await message.answer(
        await render(
            'profile/create/2_age',
            user_name=user_name,
            first_meet=(await state.get_data()).get('profile_id') is None,
        ),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(ProfileCreationStates.age)
    return bot_message


@router.message(ProfileCreationStates.name)
async def age_error(message: types.Message) -> types.Message:
    return await message.answer('Мне нужно знать твое имя')
