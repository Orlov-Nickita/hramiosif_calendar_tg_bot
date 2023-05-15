"""
Модуль с функциями для работы с базой данных SQL
"""

import sqlite3 as sq
import datetime
from loader import bot, administrators
from utils.logger import logger
from aiogram.types import Message


async def data_add(sql_base: str, message: Message) -> None:
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
        
        await bot.send_message(chat_id=administrators['Никита'],
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


async def get_info_from_sql_for_followers(sql_base: str, message: Message) -> list:
    """
    Функция, которая определяет количество записей в БД.
    :param sql_base: База данных.
    :param message: Сообщение от пользователя.
    """
    logger.info('Запущена команда sql_funcs.get_info_from_sql_for_followers',
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
        
        await bot.send_message(chat_id=administrators['Никита'],
                               text='Произошла ошибка извлечения данных из БД в функции '
                                    'get_info_from_sql_for_followers\n'
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


async def sql_hdd_root_dir_get(sql_base: str, message: Message,
                               koren: bool = False, path: bool = False) -> str:
    """
    Извлечение корневой папки для конкретного пользователя для работы с файлами на жестком диске
    :param sql_base: База данных.
    :param message: Сообщение от пользователя.
    :param koren: Для получения данных на корневую папку
    :param path: Для получения текущей директории
    """
    logger.info('Запущена команда sql_funcs.sql_hdd_root_dir_get',
                user_id=message.chat.id)
    
    try:
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            """ Таблица admin_hdd_roots
            Пользователь INTEGER,
            Имя TEXT,
            Фамилия TEXT,
            Никнейм TEXT,
            Путь TEXT,
            Корень TEXT
            """
            
            if koren:
                cursor.execute(
                    "SELECT Корень FROM admin_hdd_roots WHERE Пользователь = {id}".format(id=message.chat.id))
            
            elif path:
                cursor.execute(
                    "SELECT Путь FROM admin_hdd_roots WHERE Пользователь = {id}".format(id=message.chat.id))
            
            root_hdd = cursor.fetchone()
    
    except Exception as Exec:
        logger.error('Произошла ошибка:\n{}'.format(Exec),
                     user_id=message.chat.id)
        
        await bot.send_message(chat_id=administrators['Никита'],
                               text='Произошла ошибка извлечения данных из БД в функции sql_hdd_root_dir_get\n'
                                    '\n'
                                    '{id}\n'
                                    '{name}\n'
                                    '{f_name}\n'
                                    '{username}'.format(id=message.chat.id,
                                                        name=message.from_user.first_name,
                                                        f_name=message.from_user.last_name,
                                                        username=message.from_user.username))
    
    return root_hdd[0]


async def sql_hdd_root_dir_update(sql_base: str, root_dir: str, message: Message,
                                  koren: bool = False, path: bool = False) -> None:
    """
    Обновление корневой папки для конкретного пользователя для работы с файлами на жестком диске
    """
    logger.info('Запущена команда sql_funcs.sql_hdd_root_dir',
                user_id=message.chat.id)
    
    try:
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            """ Таблица admin_hdd_roots
            Пользователь INTEGER,
            Имя TEXT,
            Фамилия TEXT,
            Никнейм TEXT,
            Путь TEXT,
            Корень TEXT
            """
            if koren:
                cursor.execute(
                    "UPDATE admin_hdd_roots SET Корень = '{root}' WHERE Пользователь = {id}".format(root=root_dir,
                                                                                                    id=message.chat.id))
            elif path:
                cursor.execute(
                    "UPDATE admin_hdd_roots SET Путь = '{root}' WHERE Пользователь = {id}".format(root=root_dir,
                                                                                                  id=message.chat.id))
    
    except Exception as Exec:
        logger.error('Произошла ошибка:\n{}'.format(Exec),
                     user_id=message.chat.id)
        
        await bot.send_message(chat_id=administrators['Никита'],
                               text='Произошла ошибка обновления данных в БД в функции sql_hdd_root_dir_update\n'
                                    '\n'
                                    '{id}\n'
                                    '{name}\n'
                                    '{f_name}\n'
                                    '{username}'.format(id=message.chat.id,
                                                        name=message.from_user.first_name,
                                                        f_name=message.from_user.last_name,
                                                        username=message.from_user.username))
