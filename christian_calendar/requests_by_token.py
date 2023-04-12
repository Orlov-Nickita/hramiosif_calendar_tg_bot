import requests
import telebot

from utils.HTML_parser import html_to_text_parser
from excel_utils.open_check_funcs import data_from_json, data_to_json
from utils.logger import logger

apitoken = data_from_json('./christian_calendar/jsons/christ_api_token.json')['token']

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer {}'.format(apitoken),
}


def get_day_info_func(message: telebot.types.Message, user_day: str, file_to: str) -> None:
    """
    Получение всей информации на выбранный пользователем день
    param user_day: День, для которого выполняется поиск
    return: В файл записывается вся информация о запрошенном дне
    """
    logger.info('Запущена функция requests_by_token.get_day_info_func',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    params = {
        'date[exact]': '{}'.format(user_day),
    }
    
    day_info = requests.get('https://azbyka.ru/days/api/cache_dates', params=params, headers=headers).json()
    
    data_to_json(file_to, day_info)


def get_text_by_id(message: telebot.types.Message, text_id: str):
    """
    Получение текста по его id и расшифровка посредством дополнительной функции от тегов HTML
    param text_id: id текста в системе API
    return: Возвращается читаемый текст
    """
    logger.info('Запущена функция requests_by_token.get_text_by_id',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    response = requests.get('https://azbyka.ru/days/api/texts/{}'.format(text_id), headers=headers).json()
    text = html_to_text_parser(response['text'])
    
    return text


def get_holiday_by_id(message: telebot.types.Message, holiday_id: str):
    """
    Получение праздника по его id и расшифровка посредством дополнительной функции от тегов HTML
    param holiday_id: id праздника в системе API
    return: Возвращается читаемый текст
    """
    logger.info('Запущена функция requests_by_token.get_holiday_by_id',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    response = requests.get('https://azbyka.ru/days/api/holidays/{}'.format(holiday_id), headers=headers).json()
    text = html_to_text_parser(response['title'])
    
    return text
