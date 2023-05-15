"""
Модуль с пользовательскими клавиатурами
"""

import datetime
import emoji
import pytz
from loader import all_months_in_calendar
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def RKM_for_the_menu() -> ReplyKeyboardMarkup:
    """
    Клавиатура с кнопками меню бота
    :return: При нажатии отправляется сообщение в чат и бот обрабатывает полученное сообщение
    """
    rkm_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = KeyboardButton('Уточнить расписание богослужений {emoji}'.format(
        emoji=emoji.emojize(':pray:',
                            language='alias')
    ))
    # button2 = KeyboardButton('Посмотреть календарь {emoji}'.format(
    #     emoji=emoji.emojize(':clipboard:',
    #                         language='alias')
    # ))
    #
    # rkm_menu.add(button1, button2)
    rkm_menu.add(button1)
    
    return rkm_menu


def IKM_schedule_option() -> InlineKeyboardMarkup:
    """
    Клавиатура для определения варианта расписания: день, неделя, месяц.
    :return: Возвращается сообщение с кнопками для выбора даты.
    """
    ikm_schedule_option = InlineKeyboardMarkup(row_width=2)
    
    btn1 = InlineKeyboardButton(text='На конкретный день', callback_data='day')
    btn2 = InlineKeyboardButton(text='На текущую неделю', callback_data='week')
    btn3 = InlineKeyboardButton(text='На следующую неделю', callback_data='next_week')
    btn4 = InlineKeyboardButton(text='На текущий месяц', callback_data='month')
    
    ikm_schedule_option.add(btn1, btn2, btn3, btn4)
    
    return ikm_schedule_option


def IKM_date_schedule_choice(days_list: list) -> InlineKeyboardMarkup:
    """
    Клавиатура инлайн. Появляется после выбора кнопки с расписанием и предлагает выбрать день. Предварительно получает
    всю информацию из Google таблиц и обрабатывает первый столбец с датами.
    :return: Сообщение с кнопками для выбора даты.
    """
    ikm_date_schedule_choice = InlineKeyboardMarkup(row_width=2)
    
    today_digit = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d")
    month_digit = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%m"))
    
    current_date = '{day} {month}'.format(day=today_digit,
                                          month=all_months_in_calendar[month_digit - 1])
    
    days_list = days_list[days_list.index(current_date):]
    
    for every_day in range(0, len(days_list), 2):
        if every_day != days_list.index(days_list[-1]):
            ikm_date_schedule_choice.add(InlineKeyboardButton(text=days_list[every_day],
                                                              callback_data=days_list[every_day]),
                                         InlineKeyboardButton(text=days_list[every_day + 1],
                                                              callback_data=days_list[every_day + 1])
                                         )
        else:
            ikm_date_schedule_choice.add(InlineKeyboardButton(text=days_list[every_day],
                                                              callback_data=days_list[every_day])
                                         )
    
    ikm_date_schedule_choice.add(InlineKeyboardButton(text='Вернуться назад',
                                                      callback_data='return'))
    
    return ikm_date_schedule_choice


def IKM_week_schedule_choice_1() -> InlineKeyboardMarkup:
    """
    Клавиатура появляется после выбора кнопки с расписанием и предлагает выбрать месяц.
    :return: Возвращается следующая клавиатура с выбором других опций
    """
    ikm_week_schedule_choice = InlineKeyboardMarkup(row_width=1)
    
    btn1 = InlineKeyboardButton(text='Показать расписание текстом', callback_data='text_schedule_this')
    btn2 = InlineKeyboardButton(text='Прислать расписание файлом', callback_data='file_schedule_this')
    btn3 = InlineKeyboardButton(text='Вернуться назад', callback_data='return_this')
    
    ikm_week_schedule_choice.add(btn1, btn2, btn3)
    
    return ikm_week_schedule_choice


def IKM_week_schedule_choice_2() -> InlineKeyboardMarkup:
    """
    Клавиатура появляется после выбора кнопки с расписанием и предлагает выбрать месяц.
    :return: Возвращается следующая клавиатура с выбором других опций
    """
    ikm_week_schedule_choice = InlineKeyboardMarkup(row_width=1)
    
    btn1 = InlineKeyboardButton(text='Показать расписание текстом', callback_data='text_schedule_next')
    btn2 = InlineKeyboardButton(text='Прислать расписание файлом', callback_data='file_schedule_next')
    btn3 = InlineKeyboardButton(text='Вернуться назад', callback_data='return_next')
    
    ikm_week_schedule_choice.add(btn1, btn2, btn3)
    
    return ikm_week_schedule_choice


def IKM_open_schedule() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой "Открыть меню" для повторного выбора дня расписания
    :return:
    """
    ikm_open_schedule = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Открыть меню',
                                                                        callback_data='open_again'))
    
    return ikm_open_schedule


def IKM_photos_sliding() -> InlineKeyboardMarkup:
    """
    Клавиатура для фотоальбома.
    :return: Возвращается клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_photo_slide = InlineKeyboardMarkup(row_width=2)
    
    item1 = InlineKeyboardButton(
        text='< Листать фото',
        callback_data='previous')
    
    item2 = InlineKeyboardButton(
        text='Листать фото >',
        callback_data='next')
    
    ikm_photo_slide.add(item1, item2)
    
    return ikm_photo_slide
