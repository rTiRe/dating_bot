from aiogram import Router

from src.middlewares import AlbumMiddleware

router = Router()
router.message.middleware(AlbumMiddleware())
