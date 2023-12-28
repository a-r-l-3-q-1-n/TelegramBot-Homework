
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from contextlib import suppress
from Keyboards.Pagination import PaginationUploadHW, paginator


router = Router()

days = [
    ["Monday 🌤️   "],
    ["Tuesday 🌟  "],
    ["Wednesday 🍃"],
    ["Thursday ☁️ "],
    ["Friday 🥳   "]
]


@router.callback_query(PaginationUploadHW.filter(F.action.in_(["prev_w", "next_w", "prev_d", "next_d", "subject"])))
async def paginator_handler(call: CallbackQuery, callback_data: PaginationUploadHW):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    week_num = int(callback_data.week)
    week = week_num - 1 if week_num > 0 else 0

    day_num = int(callback_data.day)
    day = day_num - 1 if day_num > 0 else 0

    if callback_data.action == "next_w":
        week = week_num + 1 if week_num < 1 else week_num
        await call.answer(f"Next week 📅 - Week {week + 1}")

    elif callback_data.action == "prev_w":
        week = week_num - 1 if week_num > 0 else week_num
        await call.answer(f"This week 📅 - Week {week + 1}")

    elif callback_data.action == "next_d":
        day = day_num + 1 if day_num < (len(days) - 1) else day_num

    elif callback_data.action == "prev_d":
        day = day_num - 1 if day_num > 0 else day_num

    elif callback_data.action.startswith("subject_"):
        subject_name = callback_data.action.replace("subject_", "")

    with suppress(TelegramBadRequest):
        await call.message.edit_text(text=f"{days[day][0]}",
                                     reply_markup=await paginator(page, week, day))


@router.message(F.text.lower().contains("upload homework"))
async def upload_homework(message: Message):
    await message.answer(text=f"{days[0][0]}",
                         reply_markup=await paginator())
