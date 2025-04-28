from base64 import b64encode

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import ProfileCreationStates

@router.message(ProfileCreationStates.photo, F.photo)
async def city(
    message: types.Message,
    state: FSMContext,
    album: list[types.Message] = None,
) -> types.Message:
    if not album:
        album = []
    if len(album) > 3:
        return await message.answer('К сожалению я не могу сохранить все твои фото, отправь только 3 самых лучших')
    if not album:
        album.append(message)
    photos = {}
    for photo in album:
        photo_id = photo.photo[-1].file_id
        photo_file = await message.bot.get_file(photo_id)
        photo_bytes = await message.bot.download_file(photo_file.file_path)
        photos[photo_id] = b64encode(photo_bytes.read()).decode()
    await state.update_data(photos=photos)
    bot_message = await message.answer(
        await render('profile/create/5_city'),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Отправить координаты', request_location=True)],
            ],
            is_persistent=True,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder='Мой город...',
        ),
    )
    await state.set_state(ProfileCreationStates.city)
    return bot_message


@router.message(ProfileCreationStates.photo)
async def city_error(message: types.Message) -> types.Message:
    return await message.answer('Нет-нет, мне нужно твое фото')
