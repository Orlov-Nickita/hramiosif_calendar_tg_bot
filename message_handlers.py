import telebot.types
from telegram import ParseMode

from christian_calendar import send_information
from commands import c_start, c_help, c_keyboard, admin_panel, t_schedule
from loader import bot, administrators
from utils.logger import logger


@bot.message_handler(commands=['start'])
def send_welcome_func(message: telebot.types.Message) -> None:
    """
    Отправляет Пользователю стартовое сообщение
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype telebot.types.Message

    """
    logger.info('Запущена команда /start',
                username=message.from_user.username,
                user_id=message.chat.id)
    c_start.start(message)


@bot.message_handler(commands=['help'])
def help_command_func(message: telebot.types.Message) -> None:
    """
    Отправляет Пользователю вспомогательное сообщение с подсказками
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype telebot.types.Message

    """
    logger.info('Запущена команда /help',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    c_help.start(message)


@bot.message_handler(commands=['keyboard'])
def keyboard_open(message: telebot.types.Message) -> None:
    """
    Открывает Пользователю клавиатуру внизу
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype telebot.types.Message

    """
    logger.info('Запущена команда /keyboard',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    c_keyboard.start(message)


@bot.message_handler(commands=['admin', 'Admin'])
def admin_panel_func(message: telebot.types.Message) -> None:
    """
    Открывает панель управления для администраторов
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype telebot.types.Message

    """
    logger.info('Запущена команда /admin',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    if message.chat.id in administrators.values():
        admin_panel.start(message)
    
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='У Вас нет прав доступа')
        
        bot.send_message(chat_id=administrators['Никита'],
                         text='Пользователь '
                              'пытался получить доступ к администрированию:\n'
                              'tg_id: <code>{id}</code>\n'
                              'username: <code>{user}</code>\n'
                              'name: <code>{name}</code>\n'
                              'surname: <code>{surname}</code>\n'.format(id=message.chat.id,
                                                                         user=message.from_user.username,
                                                                         name=message.from_user.first_name,
                                                                         surname=message.from_user.last_name),
                         parse_mode=ParseMode.HTML
                         )


@bot.message_handler(content_types=['text'])
def text_func(message: telebot.types.Message):
    """
    Функция, которая реагирует на сообщение пользователя из чата.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message

    """
    logger.info('Запущена команда /text',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    if message.text.startswith('Уточнить расписание богослужений'):
        t_schedule.start(message)
    
    # elif message.text.startswith('Посмотреть календарь'):
    #     send_information.start(message)
    
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Выберите пункт меню\n')
