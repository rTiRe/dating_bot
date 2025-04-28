from base64 import b64encode

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.i18n import lazy_gettext as _

from src.handlers.profile.update.router import router
from src.templates import render
from src.states import ProfileUpdateStates, MainStates
from src.api.grpc.connections import profiles_connection
from src.handlers.menu import menu

@router.message(MainStates.menu, F.text.lower() == '3')
async def photo_send(message: types.Message, state: FSMContext) -> types.Message:
    bot_message = await message.answer(
        await render(
            'profile/create/4_photo',
            first_meet=(await state.get_data()).get('profile_id') is None,
            language_code=message.from_user.language_code,
        ),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(ProfileUpdateStates.photo)
    return bot_message


@router.message(ProfileUpdateStates.photo, F.photo)
async def photo_handlerW(
    message: types.Message,
    state: FSMContext,
    album: list[types.Message] = [],
) -> types.Message:
    if len(album) > 3:
        return await message.answer(str(_('К сожалению я не могу сохранить все твои фото, отправь только 3 самых лучших')))
    if not album:
        album.append(message)
    photos = []
    for photo in album:
        photo_id = photo.photo[-1].file_id
        photo_file = await message.bot.get_file(photo_id)
        photo_bytes = await message.bot.download_file(photo_file.file_path)
        photos.append(b64encode(photo_bytes.read()).decode())
    await profiles_connection.update(
        id=(await state.get_data()).get('profile_id'),
        image_base64_list=photos,
    )
    return await menu(message, state)


@router.message(ProfileUpdateStates.photo)
async def photo_handler_error(message: types.Message) -> types.Message:
    return await message.answer(
        str(_('Я тебя не понял. Пожалуйста, используй встроенные кнопки для ответа')),
    )
