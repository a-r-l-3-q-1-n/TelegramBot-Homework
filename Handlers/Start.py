from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from Database.Data import Database
from Keyboards.Builder import builder
from Keyboards.Reply import continue_kb, menu_kb
from Misc.States import RegisterUser
from Utils.Logger import Logger


db = Database()
logger = Logger()

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(text='Привет! 👋😁\n'
                              'Я здесь, чтобы помочь тебе с учебой. 📚📖\n'
                              'Добавляй и просматривай домашние задания твоей группы через меня. 📝\n\n'
                              'Это отличный способ всегда быть в курсе и не упустить ничего важного! ✨😊')

    if await db.get_user(message.from_user.id, "username") is None:
        await state.set_state(RegisterUser.NAME)
        await message.answer(text="Как тебя зовут? 🌟✍️",
                             reply_markup=await builder(message.from_user.full_name))
    else:
        await message.answer(text="Ты уже зарегистрирован! ✅",
                             reply_markup=continue_kb)
        await state.set_state(RegisterUser.FINAL)


@router.message(RegisterUser.NAME)
async def name(message: Message, state: FSMContext):
    try:
        if not message.text.isnumeric():
            telegram_id = message.from_user.id
            username = message.text

            await db.create_user(telegram_id, username)
            await state.set_state(RegisterUser.FINAL)

            await message.answer(text=f"{username} ты успешно прошел регистрацию! ✅",
                                 reply_markup=continue_kb)
        else:
            await message.answer(text="Имя должно состоять из букв! Попробуй еще раз. 😊✏️",
                                 reply_markup=await builder(message.from_user.full_name))

    except Exception:
        await message.answer(text="Произошла ошибка при регистрации имени.\n"
                                  "Пожалуйста, попробуй еще раз. 🚫🔄",
                             reply_markup=await builder(message.from_user.full_name))


@router.message(RegisterUser.FINAL)
async def final(message: Message, state: FSMContext):
    try:
        if message.text.lower().__contains__("продолжить"):
            await state.clear()
            await message.answer(text="Управляй своими заданиями легко! 📚",
                                 reply_markup=menu_kb)
        else:
            await message.answer(text="Нажми 'Продолжить' что бы начать ➡️",
                                 reply_markup=continue_kb)

    except Exception:
        await message.answer(text="Нажми 'Продолжить' что бы начать ➡️",
                             reply_markup=continue_kb)
