import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger as LOGGER
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.bot.handlers import routers
from app.services import Services
from app.settings import get_settings


async def telegram_bot():
    settings = get_settings()
    await Services.rabbitmq.start()
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(
            parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    for r in routers:
        dp.include_router(r)

    LOGGER.info("Bot started (polling).")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        LOGGER.info("Bot stopped.")


async def notify_user(user_id: int, text: str):
    settings = get_settings()

    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except:
        LOGGER.error(f"Message for user {user_id}, with text: {text} wasn't send")



if __name__ == "__main__":
    asyncio.run(telegram_bot())