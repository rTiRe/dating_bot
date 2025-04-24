from aiogram import Router

from src.handlers.profile import router as profile_router

default_router = Router()
router = Router()
router.include_routers(profile_router)
router.include_router(default_router)
