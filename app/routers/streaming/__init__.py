from faststream.rabbit.fastapi import RabbitRouter

from app.routers.streaming.router import router
from app.settings import SETTINGS


__all__ = ["streaming_router"]


streaming_router = RabbitRouter(url=SETTINGS.RABBITMQ_URL)
streaming_router.include_router(router)
