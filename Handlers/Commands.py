from aiogram import Router, F
from aiogram.types import Message

from Handlers.Messages import (
    MENU_TEXT, GUIDE_TEXT, LINKS_TEXT, ECHO_TEXT, CHS_ACTION_TEXT
)
from Keyboards.InlineReply import *


router = Router()


@router.message(F.text.lower().contains("to main menu"))
async def menu(message: Message):
    await message.answer(text=MENU_TEXT,
                         reply_markup=menu_kb)


@router.message(F.text.lower().contains("manage homework"))
async def homework(message: Message):
    await message.answer(text=CHS_ACTION_TEXT,
                         reply_markup=homework_kb)


@router.message(F.text.lower().contains("settings"))
async def settings(message: Message):
    await message.answer(text=CHS_ACTION_TEXT,
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
