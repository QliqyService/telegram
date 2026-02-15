from faststream.rabbit import RabbitQueue, RabbitRouter
from loguru import logger as LOGGER

from app.bot.telegram_bot import notify_user
from app.settings import SETTINGS


router = RabbitRouter(prefix=f"{SETTINGS.APP_STAND}::telegram::")


@router.subscriber(RabbitQueue(name="comment_created", durable=True))
async def on_comment_created(event: dict) -> None:
    LOGGER.debug(f"[TELEGRAM] comment_created received: {event}")

    tg_account = event.get("tg_account")
    comment_title = event.get("comment_title")
    form_public_url = event.get("form_public_url")
    comment_text = event.get("comment_text")
    created_at = event.get("created_at")
    comment_author_first_name = event.get("comment_author_first_name")
    comment_author_last_name = event.get("comment_author_last_name")

    if not comment_author_first_name:
        comment_author_first_name = "Anonymous User"

    if not comment_author_last_name:
        comment_author_last_name = ""

    text = (
        "📝 <b>New comment</b>\n\n"
        f"<b>Form:</b> <code>{form_public_url}</code>\n"
        f"<b>Comment Title:</b><code>{comment_title}</code>"
        f"<b>Comment:</b> {comment_text}\n"
        f"<b>At:</b> {created_at}"
        f"<b>From {comment_author_first_name} + {comment_author_last_name}"
    )

    try:
        await notify_user(user_id=tg_account, text=text)
    except Exception as e:
        LOGGER.warning(f"Something went wrong on notifying user: {e}")
        pass


