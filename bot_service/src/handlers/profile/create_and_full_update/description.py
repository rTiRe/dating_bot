from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import lazy_gettext as _

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import ProfileCreationStates
from src.api.grpc.protobufs import profiles_pb2

@router.message(ProfileCreationStates.interested_in, F.text.lower().in_(['парни', 'девушки', 'все равно', 'boys', 'girls', 'doesn\'t matter']))
async def description(message: types.Message, state: FSMContext) -> types.Message:
    interested_in_text = message.text.lower()
    if interested_in_text in ('парни', 'boys'):
        interested_in = profiles_pb2.Gender.GENDER_MALE
    elif interested_in_text in ('девушки', 'girls'):
        interested_in = profiles_pb2.Gender.GENDER_FEMALE
    else:
        interested_in = profiles_pb2.Gender.GENDER_DEFAULT
    await state.update_data(interested_in=interested_in)
    bot_message = await message.answer(
        await render(
            'profile/create/7_description',
            first_meet=(await state.get_data()).get('profile_id') is None,
            language_code=message.from_user.language_code,
        ),
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
    await state.set_state(ProfileCreationStates.description)
    return bot_message


@router.message(ProfileCreationStates.interested_in)
async def description_error(message: types.Message) -> types.Message:
    return await message.answer(str(_('Я тебя не понял. Используй кнопки на клавиатуре')))
