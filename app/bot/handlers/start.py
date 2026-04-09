from aiogram import Router, F
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from app.bot.handlers.link_accounts import submit_account_linking

router = Router()

keyboard_default = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 Help")],
        [KeyboardButton(text="⚙️ Link accounts")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,  # keep it visible
    input_field_placeholder="Choose an option…",
)

@router.message(CommandStart(deep_link=True))
async def start_with_link(message: Message, command: CommandObject) -> None:
    is_ok = await submit_account_linking(
        code=(command.args or "").strip(),
        telegram_id=str(message.from_user.id),
        telegram_username=message.from_user.username,
    )

    if is_ok:
        await message.answer(
            "✅ Telegram account linked successfully. You will receive notifications here.",
            reply_markup=keyboard_default,
        )
        return

    await message.answer(
        "❌ We could not link your account automatically. Open the website and try the Telegram linking button again.",
        reply_markup=keyboard_default,
    )


@router.message(CommandStart())
async def start_cmd(message: Message) -> None:
    await message.answer(
        "Hi! 👋 I'm the Qliqy bot. Open Telegram linking from your profile on the website to connect automatically.",
        reply_markup=keyboard_default,
    )

@router.message(F.text == "📌 Help")
async def help_btn(message: Message):
    await message.answer(
        "Open Telegram linking from your Qliqy profile to connect automatically, or use the manual linking option if needed.",
        reply_markup=keyboard_default
    )
