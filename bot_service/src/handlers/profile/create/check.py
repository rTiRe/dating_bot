from aiogram import F, types
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from src.handlers.profile.create.router import router
from src.templates import render
from src.states import ProfileCreationStates

@router.message(ProfileCreationStates.description, F.text)
async def check(message: types.Message, state: FSMContext) -> list[types.Message]:
    if message.text.lower() == 'пропустить':
        description = ''
    elif len(message.text) < 30:
        return await message.answer('Напиши хоть несколько слов о себе')
    else:
        description = message.text
    await state.update_data(description=description)
    data = await state.get_data()
    bot_message = await message.answer(
        'Так выглядит твоя анкета:',
        reply_markup=ReplyKeyboardRemove(),
    )
    caption = await render(
        'profile/create/8_check',
        name=data['name'],
        age=data['age'],
        city_location=data['city_location'],
        user_location=data['user_location'],
        description=data['description'],
    )
    if len(data['photos']) == 1:
        await message.answer_photo(
            photo=list(data['photos'].keys())[0],
            caption=caption,
        )
    else:
        media_group = MediaGroupBuilder(caption=caption)
        for num, photo_id in enumerate(data['photos'].keys()):
            media_group.add_photo(photo_id)
        await message.answer_media_group(media=media_group.build())
    await state.set_state(ProfileCreationStates.check)
    return bot_message


@router.message(ProfileCreationStates.description)
async def check_error(message: types.Message) -> types.Message:
    return await message.answer('Я тебя не понял. Пришли мне текст')
