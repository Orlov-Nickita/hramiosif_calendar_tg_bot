import os

import requests
from dotenv import load_dotenv

from christian_calendar.vars import christ_token_dir, christ_token_name
from excel_utils.open_check_funcs import data_to_json
from utils.logger import log_main

load_dotenv()
login = os.getenv('API_CHRIST_TOKEN_EMAIL')
password = os.getenv('API_CHRIST_TOKEN_PASSWORD')

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

json_data = {
    'email': login,
    'password': password
}


def get_token_func() -> None:
    """
    Функция получения токена с API Азбука Веры
    """
    
    log_main.info('Запущена функция _get_token.get_token_func')
    
    christ_token = requests.post('https://azbyka.ru/days/api/login', headers=headers, json=json_data).json()
    data_to_json(christ_token_dir + christ_token_name, christ_token)
    log_main.info('Создан файл {}'.format(christ_token_dir + christ_token_name))


get_token_func()
