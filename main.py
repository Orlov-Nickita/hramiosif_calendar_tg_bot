"""
Модуль отвечающий за запуск программы. Пусковой файл
"""

import os.path
from loader import log_dir, schedules_main_dir, users_sql_dir
from utils.logger import log_main
from message_handlers import *
from aiogram.utils import executor


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

    executor.start_polling(dispatcher=dp)
