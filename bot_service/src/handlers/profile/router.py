from aiogram import Router

from src.handlers.profile.create_and_full_update import router as create_router
from src.handlers.profile.update import router as update_router


router = Router()
router.include_routers(create_router, update_router)
