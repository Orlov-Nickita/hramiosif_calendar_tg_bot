import datetime

import emoji
from telebot import types

from loader import all_months_in_calendar


def RKM_for_the_menu() -> types.ReplyKeyboardMarkup:
    """
    Клавиатура с кнопками меню бота
    :return: При нажатии отправляется сообщение в чат и бот обрабатывает полученное сообщение
    """
    rkm_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton('Уточнить расписание богослужений {emoji}'.format(
        emoji=emoji.emojize(':pray:',
                            language='alias')
    ))
    button2 = types.KeyboardButton('Посмотреть календарь {emoji}'.format(
        emoji=emoji.emojize(':clipboard:',
                            language='alias')
    ))
    
    rkm_menu.add(button1, button2)
    
    return rkm_menu


def IKM_schedule_option() -> types.InlineKeyboardMarkup:
    """
    Клавиатура для определения варианта расписания: день, неделя, месяц.
    :return: Возвращается сообщение с кнопками для выбора даты.
    """
    ikm_schedule_option = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton(text='В конкретный день', callback_data='day')
    btn2 = types.InlineKeyboardButton(text='На эту неделю', callback_data='week')
    btn3 = types.InlineKeyboardButton(text='На весь месяц', callback_data='month')
    
    ikm_schedule_option.add(btn1, btn2, btn3)
    
    return ikm_schedule_option


def IKM_date_schedule_choice(days_list: list) -> types.InlineKeyboardMarkup:
    """
    Клавиатура инлайн. Появляется после выбора кнопки с расписанием и предлагает выбрать день. Предварительно получает
    всю информацию из Google таблиц и обрабатывает первый столбец с датами.
    :return: Сообщение с кнопками для выбора даты.
    """
    ikm_date_schedule_choice = types.InlineKeyboardMarkup(row_width=2)
    
    today_digit = datetime.datetime.now().strftime("%d")
    month_digit = int(datetime.datetime.now().strftime("%m"))
    
    current_date = '{day} {month}'.format(day=today_digit,
                                          month=all_months_in_calendar[month_digit - 1])
    
    days_list = days_list[days_list.index(current_date):]
    
    for every_day in range(0, len(days_list), 2):
        if every_day != days_list.index(days_list[-1]):
            ikm_date_schedule_choice.add(types.InlineKeyboardButton(text=days_list[every_day],
                                                                    callback_data=days_list[every_day]),
                                         types.InlineKeyboardButton(text=days_list[every_day + 1],
                                                                    callback_data=days_list[every_day + 1])
                                         )
        else:
            ikm_date_schedule_choice.add(types.InlineKeyboardButton(text=days_list[every_day],
                                                                    callback_data=days_list[every_day])
                                         )
    
    ikm_date_schedule_choice.add(types.InlineKeyboardButton(text='Вернуться назад',
                                                            callback_data='return'))
    
    return ikm_date_schedule_choice


def IKM_week_schedule_choice() -> types.InlineKeyboardMarkup:
    """
    Клавиатура появляется после выбора кнопки с расписанием и предлагает выбрать месяц.
    :return: Возвращается следующая клавиатура с выбором других опций
    """
    ikm_week_schedule_choice = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton(text='Показать расписание текстом', callback_data='text_schedule')
    btn2 = types.InlineKeyboardButton(text='Прислать расписание файлом', callback_data='file_schedule')
    btn3 = types.InlineKeyboardButton(text='Вернуться назад', callback_data='return')
    
    ikm_week_schedule_choice.add(btn1, btn2, btn3)
    
    return ikm_week_schedule_choice


def IKM_open_schedule() -> types.InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой "Открыть меню" для повторного выбора дня расписания
    :return:
    """
    ikm_open_schedule = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Открыть меню',
                                                                                    callback_data='open_again'))
    
    return ikm_open_schedule


def IKM_photos_sliding() -> types.InlineKeyboardMarkup:
    """
    Клавиатура для фотоальбома.
    :return: Возвращается клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_photo_slide = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(
        text='< Листать фото',
        callback_data='previous')
    
    item2 = types.InlineKeyboardButton(
        text='Листать фото >',
        callback_data='next')
    
    ikm_photo_slide.add(item1, item2)
    
    return ikm_photo_slide
