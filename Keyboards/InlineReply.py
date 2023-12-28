from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)


# =+=+=+=+= INLINE KEYBOARD =+=+=+=+=


links_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Instagram  📸", url="https://www.instagram.com/arl3q1n/")],
        [InlineKeyboardButton(text="Github 💻", url="https://github.com/a-r-l-3-q-1-n")]])


# =+=+=+=+= REPLY KEYBOARD =+=+=+=+=


continue_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Continue 🚀")]],
    resize_keyboard=True,
    input_field_placeholder="Click 'Continue' ➡️")

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Manage homework 📚📝")],
        [KeyboardButton(text="Settings ⚙️🔧")]],
    resize_keyboard=True,
    input_field_placeholder="Choose an action ➡️")

homework_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="View homework 📖"),
         KeyboardButton(text="Upload homework 📝")],
        [KeyboardButton(text="To main menu 🔙")]],
    resize_keyboard=True,
    input_field_placeholder="Choose an action ➡️")

settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Support 🛠️"),
         KeyboardButton(text="Guide 🆘"),
         KeyboardButton(text="Links 🌐")],
        [KeyboardButton(text="To main menu 🔙")]],
    resize_keyboard=True,
    input_field_placeholder="Choose an action ➡️")

remove_kb = ReplyKeyboardRemove()
