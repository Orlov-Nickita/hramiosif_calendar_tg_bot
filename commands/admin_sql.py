"""
Модуль обработки админ команды на работу с базой данных
"""

from aiogram.types import Message, ParseMode, ChatActions
from loader import bot, users_sql_dir, users_sql_file_name
from utils.logger import logger
from utils.sql_funcs import get_info_from_sql_for_followers


async def upload_sql(message: Message) -> None:
    """
    Функция для получения файла с БД.
    :param message: Сообщение от пользователя.
    :return: Файл с БД.
    """
    logger.info('Запущена функция admin_sql.upload_sql',
                username=message.chat.username,
                user_id=message.chat.id)
    
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.UPLOAD_DOCUMENT)
    
    await bot.send_document(chat_id=message.chat.id,
                            document=open(users_sql_dir + users_sql_file_name, 'rb'))
    
    logger.info('Бот отправил файл БД',
                user_id=message.chat.id)


async def followers_func(message: Message) -> None:
    """
    
    param message: Сообщение
    """
    qty_flw = await get_info_from_sql_for_followers(message=message)
    
    await bot.send_message(chat_id=message.chat.id,
                           text='Число пользователей в боте : <b>{}</b>'.format(qty_flw),
                           parse_mode=ParseMode.HTML)
    
    logger.info('Бот отправил сообщение\n"{}"'.format(message.text),
                user_id=message.chat.id)
