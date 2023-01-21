import sqlite3 as sq
import datetime

import telebot

from loader import bot, administrators
from utils.logger import logger


def data_add(sql_base: str, message: telebot.types.Message) -> None:
    """
    Функция, которая добавляет в базу данных информацию.
    :param sql_base: База данных.
    :param message: Сообщение от пользователя.
    """
    logger.info('Запущена команда sql_funcs.data_add',
                user_id=message.chat.id)
    
    date_msg = datetime.datetime.today().strftime("%d.%m.%Y")
    
    try:
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            """ Таблица bot_users
            Пользователь INTEGER,
            Дата добавления TEXT,
            Имя TEXT,
            Фамилия TEXT,
            Никнейм TEXT
            """
            
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


def get_info_from_sql(sql_base: str, message: telebot.types.Message) -> list:
    """
    Функция, которая определяет количество записей в БД.
    :param sql_base: База данных.
    :param message: Сообщение от пользователя.
    """
    logger.info('Запущена команда sql_funcs.get_info_from_sql',
                user_id=message.chat.id)
    
    date_msg = datetime.datetime.today().strftime("%d.%m.%Y")
    
    try:
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            """ Таблица bot_users
            Пользователь INTEGER,
            Дата добавления TEXT,
            Имя TEXT,
            Фамилия TEXT,
            Никнейм TEXT
            """
            
            cursor.execute(
                "SELECT Пользователь FROM bot_users")
            
            all_qty = cursor.fetchall()
            
    except Exception as Exec:
        logger.error('Произошла ошибка:\n{}'.format(Exec),
                     user_id=message.chat.id)
        
        bot.send_message(chat_id=administrators['Никита'],
                         text='Произошла ошибка извлечения данных из БД\n'
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

    return all_qty