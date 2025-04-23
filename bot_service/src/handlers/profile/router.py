from aiogram import Router

from src.handlers.profile.create import router as create_router

router = Router()
router.include_routers(create_router)
