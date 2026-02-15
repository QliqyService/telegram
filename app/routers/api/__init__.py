from app.routers.api.base import Router
from app.routers.api.telegram_bot.router import router as telegram_bot_router


__all__ = ["api_router"]

api_router = Router(prefix="/api/v1")

api_router.include_router(telegram_bot_router, prefix="/telegram_bot")
