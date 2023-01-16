import sqlite3 as sq
import datetime

import telebot

from loader import bot, administrators
from utils.logger import logger


def data_add(sql_base: str, message: telebot.types.Message) -> None:
    """
    Функция, которая добавляет в базу данных информацию. Первоначально проверяет не создана ли уже база данных и
    создает ее, если она не создана, а если ранее уже была создана, то сразу добавляет туда информацию
    :param sql_base: База данных.
    :type sql_base: Str.
    :param message: Сообщение от пользователя.
    :type message: Int.
    """
    logger.info('Запущена команда sql_adding_new_user.data_add',
                user_id=message.chat.id)
    
    try:
        date_msg = datetime.datetime.today().strftime("%d.%m.%Y")
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            cursor.execute(""" CREATE TABLE IF NOT EXISTS bot_users (
                Пользователь INTEGER,
                Дата добавления TEXT,
                Имя TEXT,
                Фамилия TEXT,
                Никнейм TEXT
                )""")
            
            cursor.execute(
                "SELECT Пользователь FROM bot_users WHERE Пользователь = {id}".format(id=message.chat.id))
            
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO bot_users VALUES ({id}, '{date}', '{name}', '{f_name}', '{username}')".format(
                        id=message.chat.id,
                        date=date_msg,
                        name=message.from_user.first_name,
                        f_name=message.from_user.last_name,
                        username=message.from_user.username))
                
                logger.info('В базу данных добавлена запись',
                            user_id=message.chat.id)
    
    except Exception as Exec:
        logger.error('Произошла ошибка:\n{}'.format(Exec),
                     user_id=message.chat.id)
        
        bot.send_message(chat_id=administrators['Никита'],
                         text='Произошла ошибка записи в базу данных\n'
                              '\n'
                              '{id}\n'
                              '{date}\n'
                              '{name}\n'
                              '{f_name}\n'
                              '{username}'.format(id=message.chat.id,
                                                  date=date_msg,
                                                  name=message.from_user.first_name,
                                                  f_name=message.from_user.last_name,
                                                  username=message.from_user.username))
