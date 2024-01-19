import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage 

from config_reader import config

from handlers import common, matrix_form

# Такой же чат бот из 12 работы, но с использвоанием конечного автомата (FinalStateMachine)

# Основная функция для запуски логирования действий и бота
async def main():
    logging.basicConfig( 
        level=logging.INFO, 
        format= "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token = config.bot_token.get_secret_value())
    print(dp.message)
    # Через роутер связываем состояния и бота
    dp.include_router(common.router)
    dp.include_router(matrix_form.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
