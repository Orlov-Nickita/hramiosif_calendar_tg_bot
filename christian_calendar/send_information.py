from datetime import date

import emoji
import pytz
import telebot
from dateutil.relativedelta import relativedelta
from telegram import ChatAction
from telegram_bot_calendar import DetailedTelegramCalendar
from telegram_bot_calendar.base import TelegramCalendar

from christian_calendar.get_usefull_info import parsing_info_from_site
from christian_calendar.keyboards_christ import IKM_christ_day_bonus
from christian_calendar.requests_by_token import get_day_info_func
from excel_utils.open_check_funcs import data_from_json, data_to_json
from utils.custom_funcs import button_text
from utils.logger import logger
from utils.photo_album_class import Photo_album
from keyboards_for_bot.keyboards import IKM_photos_sliding
from loader import bot

photos_dict_urls = {}
all_photos = Photo_album([])


def start(message: telebot.types.Message):
    """
    Функция для инициализации процесса выбора даты для сбора информации из православного календаря
    :param message: В качестве параметра передается сообщение.
    :return: Создается календарь для выбора даты
    """
    
    logger.info('Запущена функция send_information.start',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    TelegramCalendar.size_year_column = 1
    calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                              locale='ru',
                                              min_date=date.today(),
                                              max_date=date.today() + relativedelta(years=1)).build()
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text='Выберите дату',
                           reply_markup=calendar)
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def day_choice(c: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки календаря
    :param c: Параметр содержит callback_data нажатой кнопки, сначала год, затем месяц
    :return: Результатом выполнения является выбранная дата
    """
    logger.info(
        'Запущена функция day_choice, пользователь нажал на кнопку "{}"'.format(button_text(c)),
        username=c.message.from_user.username,
        user_id=c.message.chat.id)
    
    result, key, step = DetailedTelegramCalendar(calendar_id=1,
                                                 locale='ru',
                                                 min_date=date.today(),
                                                 max_date=date.today() + relativedelta(years=1)).process(
        
        c.data)
    if not result and key:
        bot.edit_message_text(
            text='Выберите дату',
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=key)
    elif result:
        logger.info('Пользователь выбрал дату {}'.format(result),
                    username=c.message.from_user.username,
                    user_id=c.message.chat.id)
        
        bot.delete_message(chat_id=c.message.chat.id,
                           message_id=c.message.message_id)
        
        send_day_info_to_chat(message=c.message, date=result)


def send_day_info_to_chat(message: telebot.types.Message, date: str):
    """
    Функция для отправки собранной информации Пользователю
    param message: Сообщение пользователя
    param date: Выбранная пользователем дата
    """
    
    logger.info('Запущена функция send_day_info_to_chat',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text='{emoji} Загружаю, пожалуйста, подождите...'.format(
                               emoji=emoji.emojize(':hourglass:',
                                                   language='alias')))
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=message.chat.id)
    
    get_day_info_func(message=message,
                      user_day=date,
                      file_to='./christian_calendar/jsons/all_day_info.json')
    
    parsing_info_from_site(message=message,
                           file_from='./christian_calendar/jsons/all_day_info.json',
                           file_to='./christian_calendar/jsons/brief_info.json')
    
    brief = data_from_json(json_file='./christian_calendar/jsons/brief_info.json')
    
    data_to_json(json_file='./christian_calendar/jsons/photo_album.json',
                 data_dict_or_list=[[saint, brief['saints_icons'][saint]] for saint in brief['saints_icons']])
    
    global all_photos
    all_photos = Photo_album(data_from_json(json_file='./christian_calendar/jsons/photo_album.json'))
    
    bot.delete_message(chat_id=message.chat.id,
                       message_id=msg.message_id)
    
    text = '{}\n' \
           '\n' \
           'Святые:\n'.format(date)
    
    for i in brief['saints_icons']:
        text += '{}\n'.format(i)
    
    text += '\n' \
            'Праздники:\n'
    
    for i in brief['holidays']:
        text += '{}\n'.format(i)
    
    msg2 = bot.send_message(chat_id=message.chat.id,
                            text=text,
                            reply_markup=IKM_christ_day_bonus([i for i in brief['texts']]))
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg2.text),
                user_id=message.chat.id)
    
    a = bot.send_photo(chat_id=message.chat.id, caption=all_photos.show()[0],
                       photo=all_photos.show()[1], reply_markup=IKM_photos_sliding())
    photos_dict_urls.update({a.message_id: all_photos})
    
    logger.info('Бот отправил фотографии',
                user_id=message.chat.id)


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'photo'
                                              and call.data == 'next'
                                              or call.data == 'previous')
def photo_slide(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки клавиатуры IKM_photos_sliding
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей направление
    прокрутки фотоальбома.
    :return: При нажатии на кнопку меняется фотография.
    """
    logger.info(
        'Запущена функция photo_slide, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    bot.send_chat_action(chat_id=call.message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    
    if call.data == 'next':
        next_photo = all_photos.next()
        bot.edit_message_media(media=telebot.types.InputMedia(type='photo',
                                                              media=next_photo[1],
                                                              caption=next_photo[0]),
                               chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               reply_markup=IKM_photos_sliding())
    
    if call.data == 'previous':
        prev_photo = all_photos.prev()
        bot.edit_message_media(media=telebot.types.InputMedia(type='photo',
                                                              media=prev_photo[1],
                                                              caption=prev_photo[0]),
                               chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               reply_markup=IKM_photos_sliding())


@bot.callback_query_handler(func=lambda call: call.message.text
                                              and 'Святые' in call.message.text
                                              and 'Праздники' in call.message.text)
def day_bonus_open_func(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработки нажатия на клавиши для вывода дополнительной информации для выбранного дня
    """
    logger.info(
        'Запущена функция day_bonus_open_func, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    print_text = ''
    temp = data_from_json('./christian_calendar/jsons/brief_info.json')['texts'][call.data]
    print(temp)
    count = 1
    for i in temp:
        print_text += f'{count}№. {i}\n' \
                      f'\n'
        count += 1
    
    msg = bot.send_message(chat_id=call.message.chat.id,
                           text='{}\n'
                                '\n'
                                '{}'.format(
                               call.data,
                               print_text))
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=call.message.chat.id)
