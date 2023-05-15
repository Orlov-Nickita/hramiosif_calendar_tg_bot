"""
Модуль обработки команды start
"""

from utils.sql_funcs import data_add
from loader import bot, users_sql_dir, users_sql_file_name
from utils.logger import logger
from keyboards_for_bot.keyboards import RKM_for_the_menu
from aiogram.types import Message


async def start(message: Message) -> None:
    """
    Функция инициализации бота.
    :param message: Сообщение от пользователя.
    :return: Запускается бот, добавляется запись в БД.
    """
    logger.info('Запущена функция c_start.start',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    msg = await bot.send_message(chat_id=message.chat.id,
                                 text='Приветствую Вас!\n'
                                      'Выберите пункт меню для продолжения\n'
                                      '\n'
                                      'Если возникнет необходимость обратиться за помощью в '
                                      'поддержку, нажмите тут /help или выберите соответствующий пункт меню внизу',
                                 reply_markup=RKM_for_the_menu())
    
    await data_add(sql_base=users_sql_dir + users_sql_file_name,
                   message=message,
                   )
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=message.chat.id)
