"""
Модуль отвечающий за запуск программы. Пусковой файл
"""

import os.path

from aiogram.utils.executor import start_polling
from bot.init_bot import set_commands
from loader import log_dir, schedules_main_dir, users_sql_dir, bot, dp
from utils.logger import log_main
from message_handlers import *


async def on_startup(dispatcher, url=None, cert=None):
    await set_commands(bot)
    logger.info("Starting connection")


async def on_shutdown(dispatcher):
    dispatcher.stop_polling()
    await dispatcher.storage.close()
    await dispatcher.wait_closed()
    logger.info("Closing connection")


if __name__ == '__main__':
    print('ok')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        log_main.info('Создана папка logs')

    if not os.path.exists(schedules_main_dir):
        os.makedirs(schedules_main_dir)
        log_main.info('Создана папка schedules')

    if not os.path.exists(users_sql_dir):
        os.makedirs(users_sql_dir)
        log_main.info('Создана папка sql')

    log_main.info('Бот запущен')

    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
