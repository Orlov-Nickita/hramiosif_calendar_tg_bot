import json
import pandas as pd

from loader import all_months_in_calendar


def remove_timestamp_from_dataframe(dt):
    """
    
    """
    if dt != '-':
        return dt.strftime('%d {}'.format(all_months_in_calendar[int(dt.strftime('%m')) - 1]))
    
    else:
        return '-'


def open_to_dict(excel_file: str) -> dict:
    """
    
    """
    new_ex_f = pd.read_excel(excel_file)
    data_from_excel = pd.DataFrame(new_ex_f)
    data_from_excel.replace({pd.NaT: '-'}, inplace=True)
    data_from_excel['Дата'] = data_from_excel['Дата'].apply(remove_timestamp_from_dataframe)
    return data_from_excel.to_dict()


def data_to_json(json_file: str, data_dict_or_list: dict or list) -> None:
    """
    
    """
    with open(json_file, 'w', encoding="utf-8") as temp_f:
        json.dump(data_dict_or_list, temp_f, indent=4, ensure_ascii=False)


def data_from_json(json_file: str) -> dict or list:
    """
    
    """
    with open(json_file, 'r', encoding='utf-8') as temp_k:
        js_dict = temp_k.read()
    return json.loads(js_dict)


def str_to_int_key(i_dict: dict) -> dict:
    """
    
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
    days_and_ind = {}
    for key in i_dict:
        if key == [key_j for key_j in i_dict.keys()][0]:
            days_and_ind = {value: int(key_2) for key_2, value in i_dict[key].items() if value != '-'}
    return days_and_ind


def to_lists_of_column(excel_dict: dict) -> tuple:
    """
    
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


def check_new_file(new_file: str, filejson: str) -> bool:
    """
    
    """
    return open_to_dict(new_file) == str_to_int_key(data_from_json(filejson))


# def update_variables_file(file_with_variables: str, lists: str) -> None:
    # with open(file_with_variables, 'w') as file:
    #     file.write('aasd')
    # with open(file_with_variables, 'w', encoding="utf-8") as temp:
    #     json.dump(lists, temp, indent=4, ensure_ascii=False)