from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.i18n import lazy_gettext as _
from grpc import RpcError, StatusCode

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import MainStates
from src.handlers.profile.create_and_full_update.name import name
from src.api.grpc.connections import accounts_connection, profiles_connection
from src.utils import answer_profile
from config import logger

logger = logger(__name__)

@router.message(F.text == '💤')
async def menu(
    message: types.Message,
    state: FSMContext,
) -> tuple[types.Message, types.Message, types.Message] | types.Message:
    await state.set_state(MainStates.default)
    state_data = await state.get_data()
    account_id = state_data.get(
        'account_id',
        (await accounts_connection.get_or_create(message.from_user.id, message.from_user.username)).id,
    )
    await state.set_data({'account_id': account_id})
    try:
        profile_data = await profiles_connection.get_by_account_id(account_id)
    except RpcError as exception:
        if exception.code() == StatusCode.NOT_FOUND:
            profile_data = {}
        else:
            logger.exception(exception)
            raise exception
    if not profile_data:
        return await name(message, state)
    else:
        await state.update_data(
            profile_id=profile_data.id,
            profile_search_data={
                'age': profile_data.age,
                'interested_in': profile_data.interested_in,
                'city_point': {
                    'lat': profile_data.city_point.lat,
                    'lon': profile_data.city_point.lon,
                } if profile_data.HasField('city_point') else {},
                'user_point': {
                    'lat': profile_data.user_point.lat,
                    'lon': profile_data.user_point.lon,
                } if profile_data.HasField('user_point') else {},
            }
        )
    introduce_message = await message.answer(
        str(_('Так выглядит твоя анкета:')),
        reply_markup=ReplyKeyboardRemove(),
    )
    profile_message = await answer_profile(message, profile_data)
    menu_message = await message.answer(
        await render('menu', language_code=message.from_user.language_code),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[
                KeyboardButton(text='1'),
                KeyboardButton(text='2'),
                KeyboardButton(text='3'),
                KeyboardButton(text='4'),
            ]],
            is_persistent=True,
            resize_keyboard=True,
            input_field_placeholder='Меню',
        ),
    )
    await state.set_state(MainStates.menu)
    return introduce_message, profile_message, menu_message