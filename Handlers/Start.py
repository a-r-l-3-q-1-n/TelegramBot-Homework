from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from Database.Data import database
from Handlers.Messages import (
    START_TEXT, ERROR_TEXT, GET_USERNAME_TEXT, INV_USERNAME_TEXT,
    SUC_REG_USER_TEXT, ALR_REG_USER_TEXT
)
from Keyboards.Builder import builder
from Keyboards.InlineReply import menu_kb
from Misc.States import AddUser


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(text=START_TEXT)

    if await database.get_user(message.from_user.id, "username") is None:

        await message.answer(text=GET_USERNAME_TEXT,
                             reply_markup=await builder(message.from_user.full_name))
        await state.set_state(AddUser.USERNAME)

    else:
        await message.answer(text=ALR_REG_USER_TEXT,
                             reply_markup=menu_kb)
        await state.clear()


@router.message(AddUser.USERNAME)
async def set_name(message: Message, state: FSMContext):
    try:
        if not message.text.isnumeric():
            await message.answer(text=f"{message.text} {SUC_REG_USER_TEXT}",
                                 reply_markup=menu_kb)

            await database.add_user(telegram_id=message.from_user.id, username=message.text)
            await state.clear()

        else:
            await message.answer(text=INV_USERNAME_TEXT,
                                 reply_markup=await builder(message.from_user.full_name))

    except Exception:
        await message.answer(text=ERROR_TEXT,
                             reply_markup=await builder(message.from_user.full_name))
