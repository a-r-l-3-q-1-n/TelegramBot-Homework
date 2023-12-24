from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def builder(text: str | list):
    build = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [build.button(text=txt) for txt in text]
    return build.as_markup(resize_keyboard=True,
                           one_time_keyboard=True)
