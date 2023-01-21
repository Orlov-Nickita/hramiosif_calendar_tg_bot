import emoji
import telebot
from telegram import ChatAction, ParseMode
from telegram_bot_calendar import DetailedTelegramCalendar

from christian_calendar.get_usefull_info import parsing_info_from_site
from christian_calendar.requests_by_token import get_day_info_func
from excel_utils.open_check_funcs import data_from_json, data_to_json
from utils.photo_album_class import Photo_album
from keyboards_for_bot.keyboards import IKM_photos_sliding, IKM_christ_day_bonus
from loader import bot

photos_dict_urls = {}
all_photos = Photo_album([])


def start(message: telebot.types.Message):
    """
    Функция для инициализации процесса выбора даты въезда в отель через календарь
    :param message: В качестве параметра передается сообщение
    :type message: telebot.types.Message
    :return: Создается календарь для выбора даты въезда
    :rtype None
    """
    
    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    
    calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                              locale='ru').build()
    bot.send_message(chat_id=message.chat.id,
                     text='Выберите дату',
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def chk_in_date_calendar(c: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки календаря
    :param c: Параметр содержит callback_data нажатой кнопки, сначала год, затем месяц
    :type c: telebot.types.CallbackQuery
    :return: Результатом выполнения является выбранная дата въезда Пользователя
    :rtype: None
    """
    result, key, step = DetailedTelegramCalendar(calendar_id=1,
                                                 locale='ru').process(c.data)
    if not result and key:
        bot.edit_message_text(
            text='Выберите дату',
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=key)
    elif result:
        bot.delete_message(chat_id=c.message.chat.id,
                           message_id=c.message.message_id)
        
        send_day_info_to_chat(message=c.message, date=result)


def send_day_info_to_chat(message: telebot.types.Message, date: str):
    msg = bot.send_message(chat_id=message.chat.id,
                           text='{emoji} Загружаю, пожалуйста, подождите...'.format(
                               emoji=emoji.emojize(':hourglass:',
                                                   language='alias')))
    
    get_day_info_func(date, './christian_calendar/jsons/all_day_info.json')
    parsing_info_from_site('./christian_calendar/jsons/all_day_info.json', './christian_calendar/jsons/brief_info.json')
    
    brief = data_from_json('./christian_calendar/jsons/brief_info.json')
    
    data_to_json('./christian_calendar/jsons/photo_album.json',
                 [[saint, brief['saints_icons'][saint]] for saint in brief['saints_icons']])
    
    global all_photos
    all_photos = Photo_album(data_from_json('./christian_calendar/jsons/photo_album.json'))
    
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
    
    bot.send_message(chat_id=message.chat.id,
                     text=text,
                     reply_markup=IKM_christ_day_bonus([i for i in brief['texts']]))
    
    a = bot.send_photo(chat_id=message.chat.id, caption=all_photos.show()[0],
                       photo=all_photos.show()[1], reply_markup=IKM_photos_sliding())
    photos_dict_urls.update({a.message_id: all_photos})


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'photo')
def photo_slide(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки клавиатуры IKM_photos_sliding
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей направление
    прокрутки фотоальбома.
    :type call: telebot.types.CallbackQuery
    :return: При нажатии на кнопку меняется фотография.
    :rtype: None
    """
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


@bot.callback_query_handler(func=lambda call: 'Святые' in call.message.text and 'Праздники' in call.message.text)
def day_bonus_open_func(call: telebot.types.CallbackQuery) -> None:
    bot.send_message(chat_id=call.message.chat.id,
                     text='{}\n'
                          '{}'.format(
                         call.data,
                         data_from_json('./christian_calendar/jsons/brief_info.json')['texts'][call.data]))
