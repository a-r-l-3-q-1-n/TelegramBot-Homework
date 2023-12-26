from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from Database.Data import database
from Keyboards.Builder import builder
from Keyboards.Reply import menu_kb
from Misc.States import RegisterUser


# =+=+= TEXT =+=+=


START_TEXT = (
    "Hi! 👋😁\n"
    "I'm here to help you with your studies. 📚📖\n"
    "Upload and view your group's homework through me.\n\n"
    "This is a great way to always stay informed and not miss anything important! ✨😊"
)

ERROR_TEXT = (
    "An error occurred during registration.\n"
    "Please, try again. 🔄"
)

USERNAME_TEXT = "Come up with a username? ✍️"

INVALID_USERNAME_TEXT = "The username must not contain numbers! Try again. 😊️"

ALREADY_REGISTERED_TEXT = "You're already registered! ✅"

SUCCESSFULLY_REGISTERED_TEXT = "you have successfully completed registration! ✅"


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(text=START_TEXT)

    if await database.get_user(message.from_user.id, "username") is None:

        await message.answer(text=USERNAME_TEXT,
                             reply_markup=await builder(message.from_user.full_name))
        await state.set_state(RegisterUser.NAME)

    else:
        await message.answer(text=ALREADY_REGISTERED_TEXT,
                             reply_markup=menu_kb)
        await state.clear()


@router.message(RegisterUser.NAME)
async def set_name(message: Message, state: FSMContext):
    try:
        if not message.text.isnumeric():
            await message.answer(text=f"{message.text} {SUCCESSFULLY_REGISTERED_TEXT}",
                                 reply_markup=menu_kb)

            await database.add_user(telegram_id=message.from_user.id, username=message.text)
            await state.clear()

        else:
            await message.answer(text=INVALID_USERNAME_TEXT,
                                 reply_markup=await builder(message.from_user.full_name))

    except Exception:
        await message.answer(text=ERROR_TEXT,
                             reply_markup=await builder(message.from_user.full_name))
