from aiogram import Router
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Database.Data import database

router = Router()


class PaginationUploadHW(CallbackData, prefix="pag"):
    action: str
    page: int
    week: int
    day: int


async def paginator(page: int = 0, week: int = 0, day: int = 0):
    builder = InlineKeyboardBuilder()

    subjects = await database.get_homework(week_id=week + 1, day_id=day + 1)
    # for subject in subjects:
    #     print(subject)

    subjects = [item['subject'] for item in subjects]
    for subject in subjects:
        print(subject)

        # builder.row(
        #     InlineKeyboardButton(text=subject, callback_data=f"subject_{subject}")
        # )

    builder.row(
        InlineKeyboardButton(text="◀️",
                             callback_data=PaginationUploadHW(action="prev_d", page=page, week=week, day=day).pack()),
        InlineKeyboardButton(text="▶️",
                             callback_data=PaginationUploadHW(action="next_d", page=page, week=week, day=day).pack()),

        InlineKeyboardButton(text="⏪",
                             callback_data=PaginationUploadHW(action="prev_w", page=page, week=week, day=day).pack()),
        InlineKeyboardButton(text=f"{week + 1}/2",
                             callback_data=PaginationUploadHW(action="", page=page, week=week, day=day).pack()),
        InlineKeyboardButton(text="⏩",
                             callback_data=PaginationUploadHW(action="next_w", page=page, week=week, day=day).pack())
    ).adjust(2, 3)

    return builder.as_markup()
