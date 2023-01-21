import time

import telebot
import emoji

from utils.sql_funcs import data_add
from loader import bot, users_sql_dir, users_sql_file_name
from utils.logger import logger
from keyboards_for_bot.keyboards import RKM_for_the_menu


def start(message: telebot.types.Message) -> None:
    """
    Функция инициализации бота.
    :param message: Сообщение от пользователя.
    :return: Запускается бот, добавляется запись в БД.
    """
    logger.info('Запущена функция c_start.start',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text='Чат-бот храма на Развилке {emoji1}\n'
                                'Я помогу уточнить расписание {emoji2} богослужений храма на конкретный день, '
                                'неделю или месяц\n'
                                '\n'
                                'Если возникнет необходимость обратиться за помощью в '
                                'поддержку, нажмите тут /help или выберите соответствующий пункт меню внизу'.format(
                               emoji1=emoji.emojize(':church:', language='alias'),
                               emoji2=emoji.emojize(':book:', language='alias')),
                           reply_markup=RKM_for_the_menu())
    
    data_add(sql_base=users_sql_dir + users_sql_file_name,
             message=message,
             )
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=message.chat.id)
