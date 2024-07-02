"""
Модуль с функциями для работы с базой данных SQL
"""

import datetime
from database.configure import db
from errors import QuestionAddError
from loader import bot, administrators
from utils.logger import logger
from aiogram.types import Message


async def data_add(message: Message) -> None:
    """
    Функция, которая добавляет в базу данных информацию.
    :param message: Сообщение от пользователя.
    """
    logger.info("Запущена команда sql_funcs.data_add", user_id=message.chat.id)

    date_msg = datetime.datetime.today().strftime("%d.%m.%Y")
    try:
        user_exist = db.user_get_by_id(user_id=message.chat.id)
        if not user_exist:
            db.user_create(
                values={
                    "user_id": message.chat.id,
                    "created_at": date_msg,
                    "first_name": message.from_user.first_name,
                    "last_name": message.from_user.last_name,
                    "username": message.from_user.username,
                }
            )
            logger.info("В базу данных добавлена запись", user_id=message.chat.id)

    except Exception as Exec:
        logger.error("Произошла ошибка:\n{}".format(Exec), user_id=message.chat.id)

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Произошла ошибка записи в базу данных\n"
            "\n"
            "{id}\n"
            "{date}\n"
            "{name}\n"
            "{f_name}\n"
            "{username}".format(
                id=message.chat.id,
                date=date_msg,
                name=message.from_user.first_name,
                f_name=message.from_user.last_name,
                username=message.from_user.username,
            ),
        )


async def get_info_from_sql_for_followers(message: Message) -> int:
    """
    Функция, которая определяет количество записей в БД.
    :param message: Сообщение от пользователя.
    """
    logger.info("Запущена команда sql_funcs.get_info_from_sql_for_followers", user_id=message.chat.id)

    date_msg = datetime.datetime.today().strftime("%d.%m.%Y")
    try:
        all_qty = db.user_all_qty_in_db()

    except Exception as Exec:
        logger.error("Произошла ошибка:\n{}".format(Exec), user_id=message.chat.id)

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Произошла ошибка извлечения данных из БД в функции "
            "get_info_from_sql_for_followers\n"
            "\n"
            "{id}\n"
            "{date}\n"
            "{name}\n"
            "{f_name}\n"
            "{username}".format(
                id=message.chat.id,
                date=date_msg,
                name=message.from_user.first_name,
                f_name=message.from_user.last_name,
                username=message.from_user.username,
            ),
        )

    else:
        return all_qty


async def sql_hdd_root_dir_get(message: Message, koren: bool = False, path: bool = False) -> str:
    """
    Извлечение корневой папки для конкретного пользователя для работы с файлами на жестком диске
    :param message: Сообщение от пользователя.
    :param koren: Для получения данных на корневую папку
    :param path: Для получения текущей директории
    """
    logger.info("Запущена команда sql_funcs.sql_hdd_root_dir_get", user_id=message.chat.id)
    r = ""
    try:
        if koren:
            r = db.hdd_get_koren_or_path(is_koren=True, user_id=message.chat.id)

        elif path:
            r = db.hdd_get_koren_or_path(is_path=True, user_id=message.chat.id)

    except Exception as Exec:
        logger.error("Произошла ошибка:\n{}".format(Exec), user_id=message.chat.id)

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Произошла ошибка извлечения данных из БД в функции sql_hdd_root_dir_get\n"
            "\n"
            "{id}\n"
            "{name}\n"
            "{f_name}\n"
            "{username}".format(
                id=message.chat.id,
                name=message.from_user.first_name,
                f_name=message.from_user.last_name,
                username=message.from_user.username,
            ),
        )

    return r


async def sql_hdd_root_dir_update(root_dir: str, message: Message, koren: bool = False, path: bool = False) -> None:
    """
    Обновление корневой папки для конкретного пользователя для работы с файлами на жестком диске
    """
    logger.info("Запущена команда sql_funcs.sql_hdd_root_dir", user_id=message.chat.id)
    try:
        if koren:
            db.hdd_update_by_id(user_id=message.chat.id, values={"coren": root_dir})
        elif path:
            db.hdd_update_by_id(user_id=message.chat.id, values={"path": root_dir})

    except Exception as Exec:
        logger.error("Произошла ошибка:\n{}".format(Exec), user_id=message.chat.id)

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Произошла ошибка обновления данных в БД в функции sql_hdd_root_dir_update\n"
            "\n"
            "{id}\n"
            "{name}\n"
            "{f_name}\n"
            "{username}".format(
                id=message.chat.id,
                name=message.from_user.first_name,
                f_name=message.from_user.last_name,
                username=message.from_user.username,
            ),
        )


async def sql_question_add(sql_base: str, question_text: str, message: Message) -> None:
    """
    Добавление вопроса в БД
    """
    logger.info("Запущена команда sql_funcs.sql_question_add", user_id=message.chat.id)

    try:
        pass
        # with sq.connect(sql_base) as database:
        #     cursor = database.cursor()
        #     """ Таблица questions
        #     Номер INTEGER PRIMARY KEY AUTOINCREMENT,
        #     Текст TEXT,
        #     Дата TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        #     """
        #     cursor.execute("INSERT INTO questions (Текст) VALUES (?)", (question_text,))

    except Exception as Exec:
        logger.error("Произошла ошибка:\n{}".format(Exec), user_id=message.chat.id)

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Произошла ошибка добавления вопроса в БД в функции sql_question_add\n"
            "{id}".format(id=message.chat.id),
        )

        raise QuestionAddError


async def sql_question_get(sql_base: str, message: Message):
    """
    Добавление вопроса в БД
    """
    logger.info("Запущена команда sql_funcs.sql_question_get", user_id=message.chat.id)
    pass
    # with sq.connect(sql_base) as database:
    #     cursor = database.cursor()
    #     """ Таблица questions
    #     Номер INTEGER PRIMARY KEY AUTOINCREMENT,
    #     Текст TEXT,
    #     Дата TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #     """
    #
    #     sql = """
    #     SELECT
    #     CASE strftime('%m', Дата)
    #         WHEN '01' THEN 'Январь'
    #         WHEN '02' THEN 'Февраль'
    #         WHEN '03' THEN 'Март'
    #         WHEN '04' THEN 'Апрель'
    #         WHEN '05' THEN 'Май'
    #         WHEN '06' THEN 'Июнь'
    #         WHEN '07' THEN 'Июль'
    #         WHEN '08' THEN 'Август'
    #         WHEN '09' THEN 'Сентябрь'
    #         WHEN '10' THEN 'Октябрь'
    #         WHEN '11' THEN 'Ноябрь'
    #         WHEN '12' THEN 'Декабрь'
    #         ELSE ''
    #     END as Month_Name,
    #     COUNT(*)
    #     FROM questions
    #     GROUP BY Month_Name
    #
    #     """
    #
    #     cursor.execute(sql)
    #     return cursor.fetchall()
