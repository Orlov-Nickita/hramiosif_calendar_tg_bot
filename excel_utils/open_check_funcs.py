"""
Модуль с функциями для работы с Excel файлом и для записи данных в JSON
"""


import json
import pandas as pd
import telebot

from loader import all_months_in_calendar, bot


def remove_timestamp_from_dataframe(dt):
    """
    Вспомогательная функция для очистки всех Timestamp из Excel файла после переноса в DataFrame в Pandas
    """
    if dt != '-':
        return dt.strftime('%d {}'.format(all_months_in_calendar[int(dt.strftime('%m')) - 1]))
    
    else:
        return '-'


def open_to_dict(excel_file: str, message: telebot.types.Message) -> dict:
    """
    Функция открывает файл Excel, убирает все пустые строчки и Timestamp, затем из DataFrame переделывает в словарь
    "Название столбца": {"Индекс (номер строки)": "Текст ячейки"}
    param excel_file: Путь до файла с Excel таблицей
    """
    new_ex_f = pd.read_excel(excel_file)
    data_from_excel = pd.DataFrame(new_ex_f)
    data_from_excel.replace({pd.NaT: '-'}, inplace=True)
    
    try:
        data_from_excel['Дата'] = data_from_excel['Дата'].apply(remove_timestamp_from_dataframe)
        
    except AttributeError:
        bot.send_message(chat_id=message.chat.id,
                         text='Произошла ошибка прочтения файла. Скорее всего некорректно внесена дата '
                              'в ячейки')
        exit()
        
    else:
        return data_from_excel.to_dict()


def data_to_json(json_file: str, data_dict_or_list: dict or list) -> None:
    """
    Функция записи информации из словаря или списка в файл в формате JSON
    param json_file: Имя или путь+имя файла куда будет запись
    param data_dict_or_list: Словарь / список
    """
    with open(json_file, 'w', encoding="utf-8") as temp_f:
        json.dump(data_dict_or_list, temp_f, indent=4, ensure_ascii=False)


def data_from_json(json_file: str) -> dict or list:
    """
    Функция выгружает из файла JSON всю информацию
    param json_file: Файл, из которого надо загрузить информацию
    """
    with open(json_file, 'r', encoding='utf-8') as temp_k:
        js_dict = temp_k.read()
    return json.loads(js_dict)


def str_to_int_key(i_dict: dict) -> dict:
    """
    Функция превращает все строковые ключи словаря в формат числа
    param i_dict: Словарь, в котором ключом является число, но оно записано в формате str, а нужно в int
    """
    for key in i_dict:
        temp_list = []
        temp_dict = {}
        for key_2 in i_dict[key]:
            temp_list.append(i_dict[key][key_2])
        for i in range(len(temp_list)):
            temp_dict.update({int(i): temp_list[i]})
        i_dict[key] = temp_dict
    return i_dict

def reversed_dict_days_and_row_index(i_dict: dict):
    """
    Функция, которая меняет местами ключ и значение
    param i_dict: Словарь, в котором надо поменять местами ключ и значение
    """
    days_and_ind = {}
    for key in i_dict:
        if key == [key_j for key_j in i_dict.keys()][0]:
            days_and_ind = {value: int(key_2) for key_2, value in i_dict[key].items() if value != '-'}
    return days_and_ind


def to_lists_of_column(excel_dict: dict) -> tuple:
    """
    Функция из принимаемого словаря (предварительно на 3 столбца) возвращает кортеж с 3 списками по каждому столбцу
    param excel_dict: Словарь из Excel файла после функции open_to_dict
    """
    date_col, saint_col, sch_col = [], [], []
    for key_i in excel_dict:
        for index in excel_dict[key_i]:
            if key_i == [key_j for key_j in excel_dict.keys()][0]:
                date_col.append(excel_dict[key_i][index])
            elif key_i == [key_j for key_j in excel_dict.keys()][1]:
                saint_col.append(excel_dict[key_i][index])
            elif key_i == [key_j for key_j in excel_dict.keys()][2]:
                sch_col.append(excel_dict[key_i][index])
    
    return date_col, saint_col, sch_col


def check_new_file(new_file: str, filejson: str, message: telebot.types.Message) -> bool:
    """
    Функция проверки нового загружаемого файла Excel и текущего записанного JSON файла
    param new_file: Новый файл Excel
    param filejson: Текущий файл с информацией JSON
    """
    return open_to_dict(new_file, message) == str_to_int_key(data_from_json(filejson))
