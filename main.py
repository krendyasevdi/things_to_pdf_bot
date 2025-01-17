from src.handlers import start_handler, handlers
import os

import asyncio
from aiogram import Bot, Dispatcher


# Запуск бота
async def main():
    bot = Bot(token=os.getenv('TOKEN_THINGS_TO_PDF'))
    dp = Dispatcher()

    dp.include_routers(start_handler.start_router)
    dp.include_routers(handlers.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
