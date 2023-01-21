import json
import os

import requests
from dotenv import load_dotenv

from loader import christ_token_name

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

christ_token = requests.post('https://azbyka.ru/days/api/login', headers=headers, json=json_data).json()

with open(christ_token_name, 'w', encoding='utf-8') as file:
    json.dump(christ_token, file, indent=4, ensure_ascii=False)
