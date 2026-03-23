from datetime import datetime
from html import escape

from faststream.rabbit import RabbitQueue, RabbitRouter
from loguru import logger as LOGGER

from app.bot.telegram_bot import notify_user
from app.settings import SETTINGS


router = RabbitRouter(prefix=f"{SETTINGS.APP_STAND}::telegram::")


def _format_created_at(value: str | None) -> str:
    if not value:
        return "-"

    try:
        parsed = datetime.fromisoformat(value)
        return parsed.strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return value


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

    form_title = event.get("form_title")
    comment_author_phone = event.get("comment_author_phone")

    safe_form_title = escape(str(form_title or "Untitled form"))
    safe_form_public_url = escape(str(form_public_url or "-"))
    safe_comment_title = escape(str(comment_title or "-"))
    safe_comment_text = escape(str(comment_text or "-")).replace("\n", "\n")
    safe_created_at = escape(_format_created_at(created_at))
    safe_author = escape(f"{comment_author_first_name} {comment_author_last_name}".strip() or "Anonymous User")
    safe_phone = escape(str(comment_author_phone or "-"))

    lines = [
        "<b>New comment received</b>",
        "",
        f"<b>Form:</b> {safe_form_title}",
        f"<b>Author:</b> {safe_author}",
        f"<b>Phone:</b> <code>{safe_phone}</code>",
        f"<b>Title:</b> {safe_comment_title}",
        f"<b>Received:</b> {safe_created_at}",
        "",
        "<b>Message:</b>",
        safe_comment_text,
    ]

    if form_public_url:
        lines.extend(
            [
                "",
                f'<a href="{safe_form_public_url}">Open public form</a>',
            ]
        )

    text = "\n".join(lines)

    try:
        await notify_user(user_id=tg_account, text=text)
    except Exception as e:
        LOGGER.warning(f"Something went wrong on notifying user: {e}")
        pass
