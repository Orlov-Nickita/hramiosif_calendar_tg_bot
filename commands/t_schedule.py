import datetime
import os.path

import telebot
from telegram import ChatAction, ParseMode

from excel_utils.open_check_funcs import data_from_json
from excel_utils.parsing_funcs import schedule_for_a_specific_day, schedule_for_some_days
from loader import bot, all_months_in_calendar, schedule_photo_week_file, schedule_photo_month_file, schedules_excel_dir
from utils.logger import logger
from keyboards_for_bot.keyboards import IKM_schedule_option, IKM_date_schedule_choice, IKM_open_schedule, \
    IKM_week_schedule_choice
from utils.custom_funcs import button_text

############################################
"""
Старт
"""


def start(message: telebot.types.Message) -> None:
    """
    Стартовая функция формирования ответа на запрос расписания
    :param message: Сообщение от пользователя из чата
    :return: Бот обрабатывает сообщение и направляет ответ
    """
    
    logger.info('Запущена функция t_schedule.start пользователь написал "{}"'.format(message.text),
                username=message.from_user.username,
                user_id=message.chat.id)
    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    
    if message.text.startswith('Уточнить расписание богослужений'):
        """
        В данном случае посылается на обработку запрос в функцию IKM_date_schedule_choice для вывода кнопок с датами
        """
        msg = bot.send_message(chat_id=message.chat.id,
                               text='Вы хотите уточнить расписание богослужений',
                               reply_markup=IKM_schedule_option())
        
        logger.info('Бот ответил "{}"'.format(msg.text),
                    user_id=message.chat.id)
    
    else:
        """
        В данном случае была введена команда, которую бот еще не понимает и потому бот отправляет сообщение с просьбой
        выбрать пункт меню
        """
        msg = bot.send_message(chat_id=message.chat.id,
                               text='Выберите пункт меню')
        
        logger.info('Бот ответил "{}"'.format(msg.text),
                    user_id=message.chat.id)


############################################
"""
Выбор из меню расписания на один день
"""


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    'Вы хотите уточнить расписание богослужений') and call.data == 'day')
def day_choice_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Выбран пункт "День"
    """
    logger.info(
        'Запущена функция day_choice_keyboard_callback пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    bot.send_chat_action(chat_id=call.message.chat.id, action=ChatAction.TYPING)
    
    days = [i for i in data_from_json(schedules_excel_dir + 'days_list.json') if i != '-']
    
    msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='На какой день Вы хотели посмотреть расписание?',
                                reply_markup=IKM_date_schedule_choice(days_list=days))
    
    logger.info('Бот ответил "{}"'.format(msg.text),
                user_id=call.message.chat.id)


############################################
"""
Отправка расписания на конкретный день
"""


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    'На какой день Вы хотели посмотреть расписание') and call.data != 'open_again')
def date_choice_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Это для меню на конкретный день
    """
    logger.info(
        'Запущена функция date_choice_keyboard_callback пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    bot.send_chat_action(chat_id=call.message.chat.id, action=ChatAction.TYPING)
    
    if call.data == 'return':
        
        logger.info('Пользователь нажал на кнопку "{}"'.format(button_text(call)),
                    username=call.message.from_user.username,
                    user_id=call.message.chat.id)
        
        bot.edit_message_text(text='Вы хотите уточнить расписание богослужений',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=IKM_schedule_option())
    
    else:
        
        logger.info('Пользователь нажал на кнопку "{}"'.format(button_text(call)),
                    username=call.message.from_user.username,
                    user_id=call.message.chat.id)
        
        msg = bot.edit_message_text(text='На какой день Вы хотели посмотреть расписание?\n'
                                         '<i>- <code>Вы выбрали {button}</code></i>'.format(
            button=button_text(call)),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_open_schedule(),
            parse_mode=ParseMode.HTML)
        
        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text),
                    user_id=call.message.chat.id)
        
        bot.send_chat_action(chat_id=call.message.chat.id, action=ChatAction.TYPING)
        
        schedule = schedule_for_a_specific_day(day=call.data,
                                               username=call.message.from_user.username,
                                               user_id=call.message.chat.id)
        
        msg = bot.send_message(chat_id=call.message.chat.id,
                               text=schedule,
                               parse_mode=ParseMode.HTML)
        
        logger.info('Пользователь нажал на кнопку "{}"'.format(button_text(call)),
                    username=call.message.from_user.username,
                    user_id=call.message.chat.id)
        
        logger.info(
            'Пользователь выбрал дату {date}'.format(date=call.data),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        
        logger.info('Бот ответил "{}"'.format(msg.text),
                    user_id=call.message.chat.id)


############################################
"""
Выбор из меню расписания на неделю
"""


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    'Вы хотите уточнить расписание богослужений') and call.data == 'week')
def week_choice_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Выбран пункт "Неделя". Предлагается выбор между текстом и файлом
    """
    
    logger.info(
        'Запущена функция week_choice_keyboard_callback пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Вы хотели посмотреть расписание на неделю. Выберите удобный вариант',
                                reply_markup=IKM_week_schedule_choice())
    
    logger.info('Бот ответил "{}"'.format(msg.text),
                user_id=call.message.chat.id)


############################################
"""
Отправка расписания на неделю
"""


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    'Вы хотели посмотреть расписание на неделю') and call.data != 'open_again')
def date_choice_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Это для меню на неделю
    """
    logger.info('Запущена функция week_choice_keyboard_callback, '
                'пользователь нажал на кнопку "{}"'.format(button_text(call)),
                username=call.message.from_user.username,
                user_id=call.message.chat.id)
    
    if call.data == 'text_schedule':
        bot.send_chat_action(chat_id=call.message.chat.id, action=ChatAction.TYPING)
        
        today_digit = datetime.datetime.now().strftime("%d")
        month_digit = int(datetime.datetime.now().strftime("%m"))
        
        current_date = '{day} {month}'.format(day=today_digit,
                                              month=all_months_in_calendar[month_digit - 1])
        
        days_till_week_end = 8 - datetime.datetime.now().isoweekday()
        all_days_in_schedule = [i for i in data_from_json(schedules_excel_dir + 'days_list.json') if i != '-']
        
        current_day = all_days_in_schedule.index(current_date)
        
        rest_week = all_days_in_schedule[current_day:current_day + days_till_week_end]
        
        bot.send_chat_action(chat_id=call.message.chat.id, action=ChatAction.TYPING)
        
        week_schedule = schedule_for_some_days(days=rest_week,
                                               username=call.message.from_user.username,
                                               user_id=call.message.chat.id,
                                               )
        
        msg = bot.send_message(chat_id=call.message.chat.id,
                               text=week_schedule,
                               parse_mode=ParseMode.HTML)
        
        logger.info('Бот ответил\n"{}"'.format(msg.text),
                    user_id=call.message.chat.id)
    
    if call.data == 'file_schedule':
        bot.send_chat_action(chat_id=call.message.chat.id, action=ChatAction.UPLOAD_PHOTO)
        
        this_week_digit = int(datetime.datetime.now().strftime("%U"))
        
        if os.path.exists(schedule_photo_week_file.format(num_week=this_week_digit)):
            bot.send_photo(chat_id=call.message.chat.id,
                           photo=open(schedule_photo_week_file.format(num_week=this_week_digit),
                                      'rb'))
            
            logger.info('Бот отправил фото week_{}.jpg'.format(this_week_digit),
                        user_id=call.message.chat.id)
        
        else:
            msg = bot.send_message(chat_id=call.message.chat.id,
                                   text='К сожалению, расписания на всю неделю в виде файла пока еще нет. Вы можете '
                                        'написать в поддержку /help и поторопить их',
                                   parse_mode=ParseMode.HTML)
            
            logger.info('Бот ответил "{}"'.format(msg.text),
                        user_id=call.message.chat.id)
    
    elif call.data == 'return':
        msg = bot.edit_message_text(text='Вы хотите уточнить расписание богослужений',
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=IKM_schedule_option())
        
        logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                    user_id=call.message.chat.id)
    
    else:
        
        bot.edit_message_text(text='Вы хотели посмотреть расписание на неделю\n'
                                   '<i>- <code>Вы выбрали {button}</code></i>'.format(
            button=button_text(call)),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_open_schedule(),
            parse_mode=ParseMode.HTML)
        
        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text),
                    user_id=call.message.chat.id)
        
        bot.send_chat_action(chat_id=call.message.chat.id, action=ChatAction.TYPING)


############################################
"""
Отправка расписания на месяц
"""


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    'Вы хотите уточнить расписание богослужений') and call.data == 'month')
def month_choice_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Выбран пункт "Месяц"
    """
    
    logger.info(
        'Запущена функция month_choice_keyboard_callback пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    bot.send_chat_action(chat_id=call.message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    
    this_month_digit = int(datetime.datetime.now().strftime("%m"))
    
    if os.path.exists(schedule_photo_month_file.format(num_month=this_month_digit)):
        bot.send_photo(chat_id=call.message.chat.id,
                       photo=open(schedule_photo_month_file.format(num_month=this_month_digit),
                                  'rb'))
        
        logger.info('Бот отправил фото month_{}.jpg'.format(this_month_digit),
                    user_id=call.message.chat.id)
    
    else:
        msg = bot.send_message(chat_id=call.message.chat.id,
                               text='К сожалению, расписания на весь месяц в виде файла пока еще нет. Вы можете '
                                    'написать в поддержку /help и поторопить их',
                               parse_mode=ParseMode.HTML)
        
        logger.info('Бот ответил "{}"'.format(msg.text),
                    user_id=call.message.chat.id)


############################################
"""
Кнопка открыть меню
"""


@bot.callback_query_handler(func=lambda call: call.data == 'open_again')
def date_open_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Обработчик нажатия на кнопку "Открыть меню" для повторного выбора дня и расписания
    """
    
    logger.info('Запущена функция date_open_keyboard_callback, '
                'пользователь нажал на кнопку "{}"'.format(button_text(call)),
                username=call.message.from_user.username,
                user_id=call.message.chat.id)
    
    if 'На какой день Вы хотели посмотреть расписание?' in call.message.text:
        all_days_in_schedule = [i for i in data_from_json(schedules_excel_dir + 'days_list.json') if i != '-']
        
        msg = bot.edit_message_text(text='На какой день Вы хотели посмотреть расписание?',
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=IKM_date_schedule_choice(days_list=all_days_in_schedule))
    
    if 'Вы хотели посмотреть расписание на неделю' in call.message.text:
        msg = bot.edit_message_text(text='Вы хотели посмотреть расписание на неделю. Выберите удобный вариант',
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=IKM_week_schedule_choice())
    
    logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text),
                user_id=call.message.chat.id)
