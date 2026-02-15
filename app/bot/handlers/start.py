from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

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

@router.message(CommandStart())
async def start_cmd(message: Message) -> None:
    await message.answer(
        "Hi! 👋I'm bot for QLIQY service. Use commands below to link you telegram account to you web page account",
        reply_markup=keyboard_default
    )

@router.message(F.text == "📌 Help")
async def help_btn(message: Message):
    await message.answer(
        "Hi! 👋I'm bot for QLIQY service. Use commands below to link you telegram account to you web page account",
        reply_markup=keyboard_default
    )