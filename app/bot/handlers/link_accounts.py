from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from loguru import logger as LOGGER
from app.bot.states.link_account import LinkAccount
from app.schemas.account_linking import TGRPCRequest, TGRPCResponse
from app.services import Services
from app.settings import SETTINGS, ServiceName

router = Router()
queue_name = f"{SETTINGS.APP_STAND}::webapi::link_account"

keyboard_default = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 Help")],
        [KeyboardButton(text="⚙️ Link accounts")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Choose an option…")

keyboard_to_cancel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Cancel")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Choose an option…")


async def submit_account_linking(*, code: str, telegram_id: str, telegram_username: str | None) -> bool:
    request_message = TGRPCRequest(
        telegram_id=telegram_id,
        code=code,
        telegram_username=telegram_username,
    )
    LOGGER.info(f"Trying to send {request_message} to {queue_name}")
    LOGGER.info(f"RABBITMQ_URL = {SETTINGS.RABBITMQ_URL!r}")
    rpc_response = await Services.rabbitmq.request(
        queue=queue_name,
        message=request_message.model_dump(mode="json"),
    )
    if rpc_response is None:
        LOGGER.error("❌ Can't get a response for account linking, aborting")
        return False

    response_data = TGRPCResponse.model_validate_json(rpc_response.body)
    return response_data.ok == str(True)

@router.message(F.text == "⚙️ Link accounts")
async def link_account(message: Message, state: FSMContext):
    await message.answer(
        "To link your web page account please reply to this message with special generated text from the web page",
        reply_markup=keyboard_to_cancel)
    await state.set_state(LinkAccount.waiting_for_code)


@router.message(F.text == "❌ Cancel")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Operation cancelled.", reply_markup=keyboard_default)


@router.message(LinkAccount.waiting_for_code)
async def process_link_code(message: Message, state: FSMContext):
    code = message.text.strip()
    is_ok = await submit_account_linking(
        code=str(code),
        telegram_id=str(message.from_user.id),
        telegram_username=message.from_user.username,
    )
    if not is_ok:
        await message.answer(
            "❌ Something went wrong. Check your code or try again later",
            reply_markup=keyboard_default,
        )
    else:
        await message.answer(
            "✅ Linking is finished. When your form will receive a comment, you will get a message.",
            reply_markup=keyboard_default,
        )
    await state.clear()
