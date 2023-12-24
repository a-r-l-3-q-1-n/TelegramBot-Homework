from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


continue_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Continue 🚀")]],
    resize_keyboard=True,
    input_field_placeholder="Click 'Continue' ➡️")

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Homework 📚📝")],
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
         KeyboardButton(text="Help 🆘"),
         KeyboardButton(text="Links 🌐")],
        [KeyboardButton(text="To main menu 🔙")]],
    resize_keyboard=True,
    input_field_placeholder="Choose an action ➡️")

remove_kb = ReplyKeyboardRemove()
