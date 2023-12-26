from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from Database.Data import database
from Keyboards.Builder import builder
from Keyboards.Reply import menu_kb
from Misc.States import SupportRequest
from Settings.Config import SUPPORT_CHAT_ID

router = Router()


@router.message(F.text.lower().contains("support"))
async def support(message: Message, state: FSMContext):
    await state.set_state(SupportRequest.MESSAGE)
    await message.answer(
        text="Describe the situation in as much detail as possible so that the admin can help you. 🔎️🌟\n\n"
             "Indicate details and circumstances that may be useful in solving the problem! 💡",
        reply_markup=await builder("Back"))


@router.message(SupportRequest.MESSAGE)
async def send_message(message: Message, state: FSMContext):
    try:
        if message.text.lower() == "back":
            await message.answer(text="Action canceled ⛔",
                                 reply_markup=menu_kb)

        else:
            username = str(await database.get_user(telegram_id=message.from_user.id, field="username"))

            print(username)
            print(message.text)

            await message.bot.send_message(chat_id=SUPPORT_CHAT_ID, text=f"User {username} sent you a message:\n"
                                                                         f"{message.text}")
            await message.answer(text="Your message has been successfully sent to the administrator!",
                                 reply_markup=menu_kb)

        await state.clear()
    except Exception:
        await message.answer(text="An error occurred while sending the message!\n"
                                  "Please, try again. 🔄")
