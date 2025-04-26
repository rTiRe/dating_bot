from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from geopy import Nominatim

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import ProfileCreationStates

geolocator = Nominatim(user_agent='dating_bot')

@router.message(ProfileCreationStates.city, F.text | F.location)
async def interested_in(message: types.Message, state: FSMContext) -> types.Message:
    city_location = {}
    user_location = {}
    if message.text:
        geocoded_city = geolocator.geocode({'city': message.text}, exactly_one=True)
        if not geocoded_city:
            return await message.answer('Похоже, такого города не существует. Пожалуйста, проверь наличие ошибок')
        city_location = {
            'name': message.text.capitalize(),
            'lat': geocoded_city.latitude,
            'lon': geocoded_city.longitude,
        }
    elif message.location:
        user_location = {
            'lat': message.location.latitude,
            'lon': message.location.longitude,
        }
    await state.update_data(city_location=city_location, user_location=user_location)
    bot_message = await message.answer(
        await render('profile/create/6_interested_in'),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Парни'),
                    KeyboardButton(text='Девушки'),
                    KeyboardButton(text='Все равно'),
                ],
            ],
            is_persistent=True,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder='Я ищу...',
        ),
    )
    await state.set_state(ProfileCreationStates.interested_in)
    return bot_message


@router.message(ProfileCreationStates.city)
async def interested_in_error(message: types.Message) -> types.Message:
    return await message.answer('Мне нужно название города или геопозиция')
