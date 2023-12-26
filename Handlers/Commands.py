from aiogram import Router, F
from aiogram.types import Message

from Keyboards.Inline import *
from Keyboards.Reply import *


# =+=+= TEXT =+=+=


MENU_TEXT = (
    "Manage your tasks easily! 📚\n"
    "Add, view homework with a single click."
)


GUIDE_TEXT = (
    "..."
)

LINKS_TEXT = (
    "Do you want to know more about the projects? 🕵️‍♂️🌟\n"
    "Visit profiles:\n"
)

CHOOSE_ACTION_TEXT = "Choose an action 🤔"

ECHO_TEXT = "Sorry, I didn't understand that command. 🤖"


router = Router()


@router.message(F.text.lower().contains("to main menu"))
async def menu(message: Message):
    await message.answer(text=MENU_TEXT,
                         reply_markup=menu_kb)


@router.message(F.text.lower().contains("manage homework"))
async def homework(message: Message):
    await message.answer(text=CHOOSE_ACTION_TEXT,
                         reply_markup=homework_kb)


@router.message(F.text.lower().contains("settings"))
async def settings(message: Message):
    await message.answer(text=CHOOSE_ACTION_TEXT,
                         reply_markup=settings_kb)


@router.message(F.text.lower().contains("guide"))
async def guide(message: Message):
    await message.answer(text=GUIDE_TEXT)


@router.message(F.text.lower().contains("links"))
async def links(message: Message):
    await message.answer(text=LINKS_TEXT,
                         reply_markup=links_kb)


@router.message()
async def echo(message: Message):
    await message.answer(text=ECHO_TEXT)
