from aiogram import F, types
from aiogram.fsm.context import FSMContext

from src.handlers.profile.create_and_full_update.router import router
from src.states import ProfileCreationStates
from src.handlers.menu import menu
from src.api.grpc.connections import profiles_connection

@router.message(ProfileCreationStates.description, F.text)
async def create(
    message: types.Message,
    state: FSMContext,
) -> tuple[types.Message, types.Message, types.Message] | types.Message:
    if message.text.lower() == 'пропустить':
        description = ''
    elif len(message.text) < 30:
        return await message.answer('Напиши хоть несколько слов о себе')
    else:
        description = message.text
    await state.update_data(description=description)
    data = await state.get_data()
    user_location = data.get('user_location')
    if user_location:
        coordinates = user_location
    else:
        coordinates = data.get('city_location')
    method_data = {
        'account_id': data.get('account_id'),
        'name': data.get('name'),
        'age': data.get('age'),
        'gender': data.get('gender'),
        'biography': data.get('description'),
        'image_base64_list': list(data.get('photos').values()),
        'coordinates': coordinates,
    }
    if data.get('profile_id') is None:
        await profiles_connection.create(**method_data)
    else:
        await profiles_connection.update(id=data.get('profile_id'), **method_data)
    return await menu(message, state)


@router.message(ProfileCreationStates.description)
async def check_error(message: types.Message) -> types.Message:
    return await message.answer('Я тебя не понял. Пришли мне текст')
