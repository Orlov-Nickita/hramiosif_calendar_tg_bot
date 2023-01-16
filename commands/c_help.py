import telebot

from loader import bot
from utils.logger import logger


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая формирует сообщение с подсказкой и отправляет Пользователю
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message
    
    """
    logger.info('Запущена функция c_help.start',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text='Бот поможет Вам узнать расписание богослужений на месяц или определённый день.\n'
                                'Воспользуйтесь меню внизу экрана\n'
                                '\n'
                                'Также Вы можете отправить одну из указанных ниже команд:\n'
                                '/help - Помощь\n'
                                '/keyboard - Открыть клавиатуру внизу экрана, если по какой-то причине она исчезла, но '
                                'также помните, что Вы можете скрывать и показывать клавиатуру принудительно, нажимая '
                                'на соответствующую кнопку в конце строки ввода текста\n'
                                ''
                                ''
                                '_________________________________________________\n'
                                'Если у Вас есть замечания или пожелания по улучшению работы Бота, '
                                'Вы можете сообщить о них в поддержку: https://t.me/+NtNLZMJ7x_o4N2U6')
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=message.chat.id)
