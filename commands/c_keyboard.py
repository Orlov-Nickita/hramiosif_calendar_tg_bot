import telebot
from loader import bot
from utils.logger import logger
from keyboards_for_bot.keyboards import RKM_for_the_menu


def start(message: telebot.types.Message) -> None:
    """
    Функция для включения клавиатуры в случае чистки диалога.
    :param message: Принимается сообщение от пользователя.
    :return: Возвращается приветственное сообщение и открывается меню бота с клавиатурой.
    """
    logger.info('Запущена функция c_keyboard.start',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text='Клавиатура открыта',
                           reply_markup=RKM_for_the_menu())
    
    logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                user_id=message.chat.id)