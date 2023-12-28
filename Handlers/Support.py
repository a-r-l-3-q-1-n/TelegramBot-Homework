from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from Database.Data import database
from Handlers.Messages import (
    SUPPORT_TEXT, ERROR_TEXT, CXL_ACTION_TEXT, SUC_MSG_SENT_TEXT
)
from Keyboards.Builder import builder
from Keyboards.InlineReply import menu_kb
from Misc.States import Support
from Settings.Config import SUPPORT_CHAT_ID


router = Router()


@router.message(F.text.lower().contains("support"))
async def support(message: Message, state: FSMContext):
    await state.set_state(Support.MESSAGE)
    await message.answer(
        text=SUPPORT_TEXT,
        reply_markup=await builder("Back"))


@router.message(Support.MESSAGE)
async def send_message(message: Message, state: FSMContext):
    try:
        if message.text.lower() == "back":
            await message.answer(text=CXL_ACTION_TEXT,
                                 reply_markup=menu_kb)

        else:
            username = await database.get_user(telegram_id=message.from_user.id, field="username")
            await message.bot.send_message(chat_id=SUPPORT_CHAT_ID, text=f"User {username} sent you a message:\n"
                                                                         f"{message.text}")
            await message.answer(text=SUC_MSG_SENT_TEXT,
                                 reply_markup=menu_kb)

        await state.clear()
    except Exception:
        await message.answer(text=ERROR_TEXT)
