"""
Модуль обработки админ команды на отправку документации
"""

import telebot
from telegram import ChatAction

from loader import bot, admin_manual_dir, admin_manual_name
from utils.logger import logger


def upload_admin_manual(message: telebot.types.Message) -> None:
    """
    Функция для получения файла с документацией.
    :param message: Сообщение от пользователя.
    :return: Файл с документацией.
    """
    logger.info('Запущена функция admin_send_manual.start',
                username=message.chat.username,
                user_id=message.chat.id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
    
    bot.send_document(chat_id=message.chat.id,
                      document=open(admin_manual_dir + admin_manual_name, 'rb'))
    
    logger.info('Бот отправил документацию',
                user_id=message.chat.id)
