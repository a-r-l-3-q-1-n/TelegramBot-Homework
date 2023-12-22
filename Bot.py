import asyncio

from aiogram import Bot, Dispatcher

from Database.Data import Database
from Settings.Config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN,
              parse_mode="HTML")
    dp = Dispatcher()
    db = Database()

    dp.startup.register(db.init_all)

    dp.include_routers(
        ...
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    try:
        print(f"[INFO] -> Bot started successfully")

        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"[INFO] -> Bot stopped via KeyboardInterrupt")
