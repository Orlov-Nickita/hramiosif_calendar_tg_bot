"""
Модуль с некоторыми данными, хранящимися в переменных
"""

import os

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

administrators = {'Никита': os.getenv('ADMINISTRATOR_NIKITA_1'),
                  "Nik": os.getenv('ADMINISTRATOR_NIKITA_2'),
                  'Саша': os.getenv('ADMINISTRATOR_SASHA'),
                  'Паша': os.getenv('ADMINISTRATOR_PASHA')}

all_months_in_calendar = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                          'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

all_months_in_calendar_for_save = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
                                   'Октябрь', 'Ноябрь', 'Декабрь']

# file name
log_file_name = 'bot_detail.log'
week_photo_name = 'week_{number}.jpg'
month_photo_name = '{month} {year}.pdf'
excel_file_name = 'xls_schedule.xlsx'
users_sql_file_name = 'users.db'
json_excel_file = 'xls_schedule_json.json'
json_days_list = 'days_list.json'
json_days_with_index = 'days_with_index.json'
json_days_with_lines = 'days_with_lines.json'
json_saints = 'saints.json'
json_timing = 'timing.json'
update_jgp = 'update.jpg'
info_jgp = 'info.jpg'
temp_error_file = 'errors.txt'
admin_manual_name = 'admin_manual.docx'

# dirs
hdd_dir = './hdd/'
admin_manual_dir = 'hdd/admin_manual/'
log_dir = './hdd/logs/'
users_sql_dir = "./hdd/sql/"
schedules_main_dir = './hdd/schedules/'
schedules_excel_dir = './hdd/schedules/excel/'
schedules_photos_dir = './hdd/schedules/photos/'
schedule_photo_week_dir = './hdd/schedules/photos/week/'
schedule_photo_month_dir = './hdd/schedules/photos/month/'
