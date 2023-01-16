from excel_utils.open_check_funcs import data_from_json
from loader import schedules_excel_dir, json_days_list, json_saints, json_timing, \
    json_days_with_index, json_days_with_lines
from utils.logger import logger


def all_days_in_schedule_file(jsonfile: str) -> dict:
    """
    Функция для получения всех строк в столбце с датой для определения даты и количества объединенных ячеек
    :return: возвращается словарь с датой в ключе и количеством пустых строк в значении
    """
    logger.info('Запущена функция how_many_days_in_schedule')
    
    dirty_days_list = data_from_json(jsonfile)
    
    day_and_lines_dict = {}
    for index, item in enumerate(dirty_days_list):
        
        if item == 'Дата':
            """
            Если содержит слово Дата, то это строка пропускается
            """
            continue
        
        if item != '-':
            """
            Если строка не пустая, то добавляет ключ в словарь и ставит значение 1
            """
            temp_item = item
            day_and_lines_dict.update(
                {item: 1}
            )
        
        else:
            """
            Если строка пустая, то добавляет к ранее добавленному значению 1
            """
            day_and_lines_dict[temp_item] += 1
    
    return day_and_lines_dict


def find_information_in_file(day: str,
                             saint: bool = False, timing: bool = False) -> str:
    """
    Функция объединяет в строку несколько ячеек, чтобы одномоментно отправить сообщение в чат.
    """
    day_index = data_from_json(schedules_excel_dir + json_days_with_index)[day]
    cell_rows = data_from_json(schedules_excel_dir + json_days_with_lines)[day]
    
    if saint:
        day_info = [i for i in data_from_json(schedules_excel_dir + json_saints)[day_index: day_index + cell_rows] if
                    i != '-']
    
    elif timing:
        day_info = [i for i in data_from_json(schedules_excel_dir + json_timing)[day_index: day_index + cell_rows] if
                    i != '-']
    
    if len(day_info) > 1:
        clean_list_day_info = [' '.join(' '.join(i.split('\n')).split()) for i in day_info if i != '-']
    
    else:
        clean_list_day_info = [' '.join(i.split()) for i in day_info[0].split('\n') if i != '-']
    
    text_to_print = '\n'.join(clean_list_day_info)
    return text_to_print


def schedule_for_a_specific_day(day: str, username: str, user_id: int) -> str:
    """
    Функция для поиска расписания и памятки на определенный день.
    :param day: День, для которого поиск.
    :param username: Никнейм для логирования.
    :param user_id: Id для логирования.
    :return: Сообщение со всей информацией на выбранных день.
    """
    logger.info('Запущена функция schedule_for_a_specific_day',
                username=username,
                user_id=user_id)
    
    if day in data_from_json(schedules_excel_dir + json_days_list):
        day_schedule = find_information_in_file(day=day,
                                                timing=True)
        saints_memorial_day = find_information_in_file(day=day,
                                                       saint=True)
        
        return '<u>{day}</u>\n' \
               '{saint}' \
               '\n' \
               '\n' \
               'Расписание:\n' \
               '{schedule}'.format(
            day=day,
            saint=saints_memorial_day,
            schedule=day_schedule)
    
    else:
        return 'На выбранный день информация в календаре отсутствует'


def schedule_for_some_days(days: list, username: str, user_id: int) -> str:
    """
    Функция для поиска расписания и памятки на определенный день.
    :param days: Дни, для которого поиск.
    :param username: Никнейм для логирования.
    :param user_id: Id для логирования.
    :return: Сообщение со всей информацией на выбранных день.
    """
    logger.info('Запущена функция schedule_for_a_specific_day',
                username=username,
                user_id=user_id)
    
    text = ''
    
    for day in days:
        if day in data_from_json(schedules_excel_dir + json_days_list):
            day_schedule = find_information_in_file(day=day,
                                                    timing=True)
            saints_memorial_day = find_information_in_file(day=day,
                                                           saint=True)
            text += '<u>{day}</u>\n' \
                    '{saint}' \
                    '\n' \
                    '\n' \
                    'Расписание:\n' \
                    '{schedule}' \
                    '\n' \
                    '\n'.format(
                day=day,
                saint=saints_memorial_day,
                schedule=day_schedule)
        
        else:
            text += 'На выбранный день информация в календаре отсутствует\n'
    
    text += '\n'
    
    return text
