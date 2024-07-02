"""
Модуль обработки админ команды на отправку документации
"""

from aiogram.types import Message, ChatActions
from loader import bot, admin_manual_dir, admin_manual_name
from utils.logger import logger


async def upload_admin_manual(message: Message) -> None:
    """
    Функция для получения файла с документацией.
    :param message: Сообщение от пользователя.
    :return: Файл с документацией.
    """
    logger.info("Запущена функция admin_send_manual.start", username=message.chat.username, user_id=message.chat.id)

    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.UPLOAD_DOCUMENT)

    await bot.send_document(chat_id=message.chat.id, document=open(admin_manual_dir + admin_manual_name, "rb"))

    logger.info("Бот отправил документацию", user_id=message.chat.id)
