from html import escape

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

    safe_form_public_url = escape(str(form_public_url or "-"))
    safe_comment_title = escape(str(comment_title or "-"))
    safe_comment_text = escape(str(comment_text or "-"))
    safe_created_at = escape(str(created_at or "-"))
    safe_author = escape(f"{comment_author_first_name} {comment_author_last_name}".strip() or "Anonymous User")

    text = (
        "📝 <b>New comment</b>\n\n"
        f"<b>Form:</b> <code>{safe_form_public_url}</code>\n"
        f"<b>Comment title:</b> <code>{safe_comment_title}</code>\n"
        f"<b>Comment:</b> {safe_comment_text}\n"
        f"<b>At:</b> {safe_created_at}\n"
        f"<b>From:</b> {safe_author}"
    )

    try:
        await notify_user(user_id=tg_account, text=text)
    except Exception as e:
        LOGGER.warning(f"Something went wrong on notifying user: {e}")
        pass

