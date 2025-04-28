from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import lazy_gettext as _

from src.handlers.profile.update.router import router
from src.templates import render
from src.states import ProfileUpdateStates, MainStates
from src.api.grpc.connections import profiles_connection
from src.handlers.menu import menu

@router.message(MainStates.menu, F.text.lower() == '2')
async def description_sender(message: types.Message, state: FSMContext) -> types.Message:
    bot_message = await message.answer(
        await render('profile/create/7_description', language_code=message.from_user.language_code),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=str(_('Пропустить')))],
            ],
            is_persistent=True,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder=str(_('Я - это ...')),
        ),
    )
    await state.set_state(ProfileUpdateStates.description)
    return bot_message


@router.message(ProfileUpdateStates.description, F.text)
async def description_handler_error(message: types.Message, state: FSMContext) -> types.Message:
    if message.text.lower() in ('пропустить', 'continue'):
        description = ''
    elif len(message.text) < 30:
        return await message.answer(str(_('Напиши хоть несколько слов о себе')))
    else:
        description = message.text
    await profiles_connection.update(
        id=(await state.get_data()).get('profile_id'),
        biography=description,
    )
    return await menu(message, state)


@router.message(ProfileUpdateStates.description)
async def description_handler_error(message: types.Message) -> types.Message:
    return await message.answer(str(_('Я тебя не понял. Пришли мне текст')))
