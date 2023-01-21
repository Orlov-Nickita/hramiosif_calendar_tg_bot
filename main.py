import os.path

from loader import log_dir, schedules_main_dir, users_sql_dir, users_sql_file_name
from message_handlers import *
from utils.logger import log_main
import sqlite3 as sq

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
        
    if not os.path.exists(users_sql_dir + users_sql_file_name):
        base = open(users_sql_dir + users_sql_file_name, 'w')
        base.close()
        log_main.info('Создан файл БД {}'.format(users_sql_dir + users_sql_file_name))

    log_main.info('Бот запущен')

    with sq.connect(users_sql_dir + users_sql_file_name) as database:
        cursor = database.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS bot_users (
            Пользователь INTEGER,
            Дата добавления TEXT,
            Имя TEXT,
            Фамилия TEXT,
            Никнейм TEXT
            )""")

    bot.infinity_polling()
