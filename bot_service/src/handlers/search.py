import asyncio

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import lazy_gettext as _

from src.handlers.router import router
from src.api.grpc.connections import recommendations_connection, profiles_connection, accounts_connection, interactions_connection
from src.handlers.menu import menu
from src.storage.redis import redis
from src.utils import answer_profile
from src.states import MainStates
from src.storage import rabbit

@router.message(F.text.lower() == '1')
async def show_buttons(message: types.Message, state: FSMContext) -> tuple[types.Message, types.Message]:
    buttons_message = await message.answer(
        text='🔍',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='❤️'),
                    KeyboardButton(text='👎'),
                    KeyboardButton(text='💤'),
                ],
            ],
            resize_keyboard=True,
            is_persistent=True,
            input_field_placeholder=str(_('Выбор:')),
        ),
    )
    return buttons_message, await search(message, state)

@router.message(MainStates.search, F.text.lower().in_(('❤️', '👎')))
async def search(message: types.Message, state: FSMContext) -> types.Message:
    state_data = await state.get_data()
    profile_search_data = state_data.get('profile_search_data')
    if not profile_search_data:
        return await menu(message, state)
    profile_id = state_data.get('profile_id')
    if message.text.lower() == '❤️':
        await rabbit.publish_like(
            liker_id=profile_id,
            liked_id=state_data['current_profile_id'],
        )
        await asyncio.sleep(2)
        for like in list((await interactions_connection.get_mutal_likes(user_id=state_data['current_profile_id'])).mutual_likes):
            if not (like.user1 in (profile_id, state_data['current_profile_id']) and like.user2 in (profile_id, state_data['current_profile_id'])):
                liked_profile_data = await profiles_connection.get_by_profile_id(state_data['current_profile_id'])
                account_data = await accounts_connection.get_by_id(liked_profile_data.account_id)
                mutal_message = await message.bot.send_message(chat_id=account_data.telegram_id, text='Вас лайкнули!')
                await answer_profile(mutal_message, await profiles_connection.get_by_profile_id(profile_id))
                break
    elif message.text.lower() == '👎':
        await rabbit.publish_dislike(
            liker_id=profile_id,
            liked_id=state_data['current_profile_id'],
        )
    next_profile_id: bytes = await redis.lpop(profile_id)
    if not next_profile_id:
        searched_profiles = await recommendations_connection.search_profiles(
            gender=profile_search_data['interested_in'],
            age=profile_search_data['age'],
            city_point=profile_search_data['city_point'],
            user_point=profile_search_data['user_point'],
            searcher_id=profile_id,
        )
        await redis.rpush(profile_id, *list(searched_profiles.profile_ids))
        await redis.expire(profile_id, 600)
        next_profile_id: bytes = await redis.lpop(profile_id)
    if next_profile_id:
        next_profile_id = next_profile_id.decode()
    else:
        profiles_end_message = await message.answer('Анкеты закончились, приходи позже')
        await menu(message, state)
        return profiles_end_message
    profile_data = await profiles_connection.get_by_profile_id(next_profile_id)
    profile_message = await answer_profile(message, profile_data)
    await state.set_state(MainStates.search)
    await state.update_data(current_profile_id=profile_data.id)
    return profile_message

