from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


continue_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Продолжить 🚀")]],
    resize_keyboard=True,
    input_field_placeholder="Нажми 'Продолжить' ➡️")

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Домашнее задание 📚📝")],
        [KeyboardButton(text="Настройки ⚙️🔧")]],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие ➡️")

homework_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Смотреть ДЗ 📖"),
         KeyboardButton(text="Загрузить ДЗ 📝")],
        [KeyboardButton(text="В главное меню 🔙")]],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие ➡️")

settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ЦПП 🛠️"),
         KeyboardButton(text="Обучение 🆘"),
         KeyboardButton(text="Ссылки 🌐")],
        [KeyboardButton(text="В главное меню 🔙")]],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие ➡️")

remove_kb = ReplyKeyboardRemove()
