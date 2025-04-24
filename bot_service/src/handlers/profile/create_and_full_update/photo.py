from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.handlers.profile.create_and_full_update.router import router
from src.templates import render
from src.states import ProfileCreationStates
from src.api.grpc.protobufs import profiles_pb2

@router.message(
    ProfileCreationStates.gender,
    F.text.lower().in_(['я парень', 'я девушка']),
)
async def photo(message: types.Message, state: FSMContext) -> types.Message:
    if message.text.lower() == 'я парень':
        await state.update_data(gender=profiles_pb2.Gender.GENDER_MALE)
    else:
        await state.update_data(gender=profiles_pb2.Gender.GENDER_FEMALE)
    bot_message = await message.answer(
        await render(
            'profile/create/4_photo',
            first_meet=(await state.get_data()).get('profile_id') is None,
        ),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(ProfileCreationStates.photo)
    return bot_message


@router.message(ProfileCreationStates.gender)
async def photo_error(message: types.Message) -> types.Message:
    return await message.answer(
        'Я тебя не понял. Пожалуйста, используй встроенные кнопки для ответа',
    )
