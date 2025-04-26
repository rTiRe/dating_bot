import asyncio
from typing import Any, Dict, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    album_data = {}

    def collect_album_messages(self, event: Message):
        if event.media_group_id not in self.album_data:
            self.album_data[event.media_group_id] = {'messages': []}
        self.album_data[event.media_group_id]['messages'].append(event)
        return len(self.album_data[event.media_group_id]['messages'])

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)
        total_before = self.collect_album_messages(event)
        await asyncio.sleep(0.1)
        total_after = len(self.album_data[event.media_group_id]['messages'])
        if total_before != total_after:
            return
        album_messages = self.album_data[event.media_group_id]['messages']
        album_messages.sort(key=lambda x: x.message_id)
        data['album'] = album_messages
        del self.album_data[event.media_group_id]
        return await handler(event, data)
