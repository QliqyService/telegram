import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger as LOGGER
from starlette.staticfiles import StaticFiles

from app.bot.telegram_bot import telegram_bot
from app.routers import *
from app.services import Services
from app.settings import get_settings


class Application(FastAPI):
    """Setting up and preparing the launch of the service"""

    def __init__(self):
        self.settings = get_settings()
        self.services = Services()
        self.logger = self.settings.configure_logging()

        super().__init__(
            title=self.settings.APP_TITLE,
            description=self.settings.APP_DESCRIPTION,
            root_path=self.settings.APP_PUBLIC_PATH,
            root_path_in_servers=True,
            docs_url="/",
            openapi_url="/openapi.json",
            redoc_url="/v1/docs",
            version=self.settings.APP_RELEASE,
        )
        self.run_startup_actions()

    def run_startup_actions(self) -> None:
        self.add_middlewares()
        self.include_routers()
        self.include_router(shared_router)
        self.add_startup_event_handlers()

    def mount_static(self) -> None:
        self.mount("/static", StaticFiles(directory="app/static"), name="static")

    def include_routers(self) -> None:
        self.include_router(streaming_router)
        LOGGER.debug("[MAIN] Routers added")

    def add_middlewares(self) -> None:
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        LOGGER.debug("[MAIN] Middlewares added")

    def add_startup_event_handlers(self) -> None:
        services = self.services.get_external_services()
        for service in services:
            self.add_event_handler("startup", service.start)
            LOGGER.debug(f"[MAIN] Started: {service}")
        self.add_event_handler("startup", self._start_telegram_bot_background)
        self.add_event_handler("shutdown", self._stop_telegram_bot_background)
        LOGGER.debug("[MAIN] Started Telegram Bot (background)")

    async def _start_telegram_bot_background(self) -> None:
        task = asyncio.create_task(telegram_bot())
        setattr(self.state, "telegram_bot_task", task)

    async def _stop_telegram_bot_background(self) -> None:
        task = getattr(self.state, "telegram_bot_task", None)
        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


app = Application()
