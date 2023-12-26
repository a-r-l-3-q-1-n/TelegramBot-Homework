import asyncio

from aiogram import Bot, Dispatcher

from Database.Data import database
from Handlers import Commands, Start, Support
from Settings.Config import BOT_TOKEN
from Utils.Logger import logger


async def main():
    bot = Bot(token=BOT_TOKEN,
              parse_mode="HTML")
    dp = Dispatcher()

    dp.startup.register(database.init_all)

    dp.include_routers(

        Start.router,
        Support.router,
        Commands.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=database)


if __name__ == "__main__":
    try:
        logger.log_info(f"[INFO] -> Bot started successfully")

        asyncio.run(main())
    except KeyboardInterrupt:
        logger.log_info(f"[INFO] -> Bot stopped via KeyboardInterrupt\n")
