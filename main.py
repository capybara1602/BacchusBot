import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from Keyboard.main_menu import set_main_menu
from log.logging import bot_logger


async def main():

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token,
            parse_mode='HTML')
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot) 
    
    bot_logger.warning("BOT WAS STARTED")


if __name__ == '__main__':
    asyncio.run(main())
       