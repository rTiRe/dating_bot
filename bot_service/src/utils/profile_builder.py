from base64 import b64decode

from aiogram.types import Message, BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from src.api.grpc.protobufs.profiles import profiles_pb2
from src.templates import render

async def answer_profile(message: Message, profile_data: profiles_pb2.ProfilesGetResponse) -> Message:
    caption = await render(
        'profile/profile',
        name=profile_data.name,
        age=profile_data.age,
        city_location=profile_data.city_point if profile_data.HasField('city_point') else None,
        user_location=profile_data.user_point if profile_data.HasField('user_point') else None,
        description=profile_data.biography,
    )
    if len(profile_data.image_base64_list) == 1:
        profile_message = await message.answer_photo(
            photo=BufferedInputFile(b64decode(profile_data.image_base64_list[0]), f'{profile_data.id}_0'),
            caption=caption,
        )
    else:
        media_group = MediaGroupBuilder(caption=caption)
        for num, photo_base64 in enumerate(profile_data.image_base64_list):
            media_group.add_photo(
                BufferedInputFile(b64decode(photo_base64), f'{profile_data.id}_{num}'),
            )
        profile_message = await message.answer_media_group(media=media_group.build())
    return profile_message
