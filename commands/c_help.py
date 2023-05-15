"""
Модуль обработки команды help
"""

from aiogram.types import Message
from loader import bot
from utils.logger import logger


async def start(message: Message) -> None:
    """
    Функция, которая формирует сообщение с подсказкой и отправляет Пользователю.
    :param message: В качестве параметра передается сообщение из чата.
    :return: Сообщение в чат.
    """
    logger.info('Запущена функция c_help.start',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    msg = await bot.send_message(chat_id=message.chat.id,
                                 text='Вы можете отправить команду:\n'
                                      '/keyboard - открыть клавиатуру внизу экрана. '
                                      'Также Вы можете скрывать и показывать клавиатуру принудительно, '
                                      'нажимая на соответствующую кнопку в конце строки ввода текста\n'
                                      '____________________________\n'
                                      'Если у Вас есть замечания или пожелания по улучшению работы Бота, '
                                      'Вы можете сообщить о них в поддержку: https://t.me/+NtNLZMJ7x_o4N2U6')
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=message.chat.id)
