from base64 import b64decode
from time import time

from aiogram import F, types
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from grpc import RpcError, StatusCode

from src.handlers.profile.create.router import router
from src.templates import render
from src.states import MainStates
from src.handlers.profile.create.name import name
from src.api.grpc.connections import accounts_connection, profiles_connection
from config import logger

logger = logger(__name__)

@router.message(F.text == '💤')
async def menu(
    message: types.Message,
    state: FSMContext,
) -> tuple[types.Message, types.Message, types.Message] | types.Message:
    await state.set_state(default_state)
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
    introduce_message = await message.answer(
        'Так выглядит твоя анкета:',
        reply_markup=ReplyKeyboardRemove(),
    )
    caption = await render(
        'profile/profile',
        name=profile_data.first_name,
        age=profile_data.age,
        # city_location=profile_data['city_location'],
        # user_location=profile_data['user_location'],
        description=profile_data.biography,
    )
    if len(profile_data.image_base64_list) == 1:
        profile_message = await message.answer_photo(
            photo=b64decode(profile_data.image_base64_list[0]),
            caption=caption,
        )
    else:
        media_group = MediaGroupBuilder(caption=caption)
        for num, photo_base64 in enumerate(profile_data.image_base64_list):
            media_group.add_photo(
                types.BufferedInputFile(b64decode(photo_base64), f'{account_id}_{int(time() * 100)}_{num}'),
            )
        profile_message = await message.answer_media_group(media=media_group.build())
    menu_message = await message.answer(
        await render('menu'),
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