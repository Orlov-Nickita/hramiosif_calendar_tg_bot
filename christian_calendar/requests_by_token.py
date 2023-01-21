import json
import requests

from christian_calendar.HTML_parser import html_to_text_parser
from excel_utils.open_check_funcs import data_from_json
from bs4 import BeautifulSoup

apitoken = data_from_json('christ_api_token.json')['token']

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer {}'.format(apitoken),
}

def request_day_info_func(user_day: str) -> None:
    """
    Получение всей информации на выбранный пользователем день
    param user_day: День, для которого выполняется поиск
    return: В файл записывается вся информация о запрошенном дне
    """
    
    params = {
        'date[exact]': '{}'.format(user_day),
    }
    
    day_info = requests.get('https://azbyka.ru/days/api/cache_dates', params=params, headers=headers).json()
    
    with open('christ_day.json', 'w', encoding='utf-8') as file:
        json.dump(day_info, file, indent=4, ensure_ascii=False)


def get_text_by_id(text_id: str):
    response = requests.get('https://azbyka.ru/days/api/texts/{}'.format(text_id), headers=headers).json()
    # soup = BeautifulSoup(response['text'])
    # print(soup.get_text())
    return print(html_to_text_parser(response['text']))
    # return soup.get_text()


# print(get_text_by_id('568'))
# print(get_text_by_id('568'))