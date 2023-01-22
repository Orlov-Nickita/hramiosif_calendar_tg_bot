import emoji
from telebot import types


def IKM_admin_panel_short() -> types.InlineKeyboardMarkup:
    """
    Клавиатура для панели управления с определенными действиями.
    :return: Возвращается клавиатура.
    """
    ikm_admin_panel_short = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton(
        text='{emoji} JPG|PNG фото расписания на неделю'.format(
            emoji=emoji.emojize(':camera:',
                                language='alias')),
        callback_data='upload_week_photo')
    
    btn2 = types.InlineKeyboardButton(
        text='{emoji} PDF файл расписания на месяц'.format(
            emoji=emoji.emojize(':camera:',
                                language='alias')),
        callback_data='upload_month_photo')
    
    btn3 = types.InlineKeyboardButton(
        text='{emoji} Excel файл расписания на месяц'.format(
            emoji=emoji.emojize(':bookmark_tabs:',
                                language='alias')),
        callback_data='upload_excel_file')
    
    btn4 = types.InlineKeyboardButton(
        text='{emoji} Подписчики'.format(
            emoji=emoji.emojize(':restroom:',
                                language='alias')),
        callback_data='followers')
    
    ikm_admin_panel_short.add(btn1, btn2, btn3, btn4)
    
    return ikm_admin_panel_short


def IKM_admin_panel_main() -> types.InlineKeyboardMarkup:
    """
    Клавиатура для панели управления со всеми функциями для главного администратора.
    :return: Возвращается клавиатура.
    """
    ikm_admin_panel_main = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton(
        text='{emoji} JPG|PNG фото расписания на неделю'.format(
            emoji=emoji.emojize(':camera:',
                                language='alias')),
        callback_data='upload_week_photo')
    
    btn2 = types.InlineKeyboardButton(
        text='{emoji} PDF файл расписания на месяц'.format(
            emoji=emoji.emojize(':camera:',
                                language='alias')),
        callback_data='upload_month_photo')
    
    btn3 = types.InlineKeyboardButton(
        text='{emoji} Excel файл расписания на месяц'.format(
            emoji=emoji.emojize(':bookmark_tabs:',
                                language='alias')),
        callback_data='upload_excel_file')
    
    btn4 = types.InlineKeyboardButton(
        text='{emoji} Прислать файл БД'.format(
            emoji=emoji.emojize(':passport_control:',
                                language='alias')),
        callback_data='sql_bd_download')
    
    btn5 = types.InlineKeyboardButton(
        text='{emoji} Проверить ошибки лог-файла'.format(
            emoji=emoji.emojize(':interrobang:',
                                language='alias')),
        callback_data='logs_check_errors')
    
    btn6 = types.InlineKeyboardButton(
        text='{emoji} Прислать лог-файл'.format(
            emoji=emoji.emojize(':blue_book:',
                                language='alias')),
        callback_data='logs_download')
    
    btn7 = types.InlineKeyboardButton(
        text='{emoji} Очистить лог-файл'.format(
            emoji=emoji.emojize(':recycle:',
                                language='alias')),
        callback_data='logs_trash')
    
    btn8 = types.InlineKeyboardButton(
        text='{emoji} Подписчики'.format(
            emoji=emoji.emojize(':restroom:',
                                language='alias')),
        callback_data='followers')
    
    btn9 = types.InlineKeyboardButton(
        text='{emoji} Сообщить об обновлениях'.format(
            emoji=emoji.emojize(':boom:',
                                language='alias')),
        callback_data='send_update_message')
    
    ikm_admin_panel_main.add(btn1, btn2, btn3, btn4,
                             btn5, btn6, btn7, btn8, btn9)
    
    return ikm_admin_panel_main


def IKM_admin_week_save_photo() -> types.InlineKeyboardMarkup:
    """
    Клавиатура для присвоения названия для фото для недельного расписания.
    :return: Возвращается клавиатура.
    """
    ikm_admin_week_save_photo = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton(text='Текущая', callback_data='this_week')
    btn2 = types.InlineKeyboardButton(text='Следующая', callback_data='next_week')
    btn3 = types.InlineKeyboardButton(text='Другая неделя', callback_data='other_week')
    
    ikm_admin_week_save_photo.add(btn1, btn2, btn3)
    
    return ikm_admin_week_save_photo


def IKM_admin_month_save_photo() -> types.InlineKeyboardMarkup:
    """
    Клавиатура для присвоения названия для фото.
    :return: Возвращается клавиатура.
    """
    ikm_admin_month_save_photo = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton(text='Текущий', callback_data='this_month')
    btn2 = types.InlineKeyboardButton(text='Следующий', callback_data='next_month')
    btn3 = types.InlineKeyboardButton(text='Другой месяц', callback_data='other_month')
    
    ikm_admin_month_save_photo.add(btn1, btn2, btn3)
    
    return ikm_admin_month_save_photo


def IKM_admin_save_photo_again() -> types.InlineKeyboardMarkup:
    """
    Отправить еще фото или закрыть меню для месячного расписания.
    :return: Возвращается клавиатура.
    """
    ikm_admin_save_photo_again = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton(text='Отправить еще', callback_data='load_again')
    btn2 = types.InlineKeyboardButton(text='Закрыть меню', callback_data='close')
    
    ikm_admin_save_photo_again.add(btn1, btn2)
    
    return ikm_admin_save_photo_again


def IKM_admin_overwrite_file_first_choice() -> types.InlineKeyboardMarkup:
    """
    Клавиатура с возможностью оценить перезаписываемый файл.
    :return: Возвращается клавиатура.
    """
    ikm_admin_overwrite_file_first_choice = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton(text='Перезаписать', callback_data='yes_overwrite')
    btn2 = types.InlineKeyboardButton(text='Нет, посмотреть файл перед удалением', callback_data='no_overwrite')
    
    ikm_admin_overwrite_file_first_choice.add(btn1, btn2)
    
    return ikm_admin_overwrite_file_first_choice


def IKM_admin_overwrite_file_second_choice() -> types.InlineKeyboardMarkup:
    """
    Клаивиатура с возможностью перезаписать или оставить имеющийся файл.
    :return: Возвращается клавиатура.
    """
    ikm_admin_overwrite_file_second_choice = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton(text='Да, перезаписать', callback_data='yes_overwrite_final')
    btn2 = types.InlineKeyboardButton(text='Нет, оставить', callback_data='no_overwrite_final')
    
    ikm_admin_overwrite_file_second_choice.add(btn1, btn2)
    
    return ikm_admin_overwrite_file_second_choice


def IKM_admin_overwrite_excel_file() -> types.InlineKeyboardMarkup:
    """
    Клаиватура с возможностью перезаписать или сотавить имеющийся файл Excel.
    :return: Возвращается клавиатура.
    """
    ikm_admin_overwrite_excel_file = types.InlineKeyboardMarkup(row_width=1)
    
    btn1 = types.InlineKeyboardButton(text='Да, перезаписать', callback_data='yes_overwrite_excel')
    btn2 = types.InlineKeyboardButton(text='Нет, оставить', callback_data='no_leave_excel')
    
    ikm_admin_overwrite_excel_file.add(btn1, btn2)
    
    return ikm_admin_overwrite_excel_file


def IKM_admin_check_hdd(files: list) -> types.InlineKeyboardMarkup:
    """
    Меню управления файловой системой на жестком диске.
    :return: Возвращается клавиатура.
    """
    ikm_admin_check_hdd = types.InlineKeyboardMarkup(row_width=1)
    
    for file in files:
        ikm_admin_check_hdd.add(types.InlineKeyboardButton(text=file,
                                                           callback_data=file)
                                )
    
    return ikm_admin_check_hdd


def IKM_admin_open_menu() -> types.InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой "Открыть меню" для открытия панели управления
    :return:
    """
    ikm_admin_open_menu = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Открыть меню',
                                                                                      callback_data='open_menu_again'))
    
    return ikm_admin_open_menu


def IKM_admin_log_remove_conf() -> types.InlineKeyboardMarkup:
    """
    Подтверждение очистки лог файла.
    :return: Клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_admin_log_remove_conf = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(
        text='Да',
        callback_data='yes_remove_log')
    
    item2 = types.InlineKeyboardButton(
        text='Нет',
        callback_data='no_remove_log')
    
    ikm_admin_log_remove_conf.add(item1, item2)
    
    return ikm_admin_log_remove_conf


def IKM_admin_update_send_conf() -> types.InlineKeyboardMarkup:
    """
    Подтверждение отправки сообщений с обновлениями.
    :return: Клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_admin_update_send_conf = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(
        text='Да',
        callback_data='yes_send_upd_msg')
    
    item2 = types.InlineKeyboardButton(
        text='Нет',
        callback_data='no_send_upd_msg')
    
    ikm_admin_update_send_conf.add(item1, item2)
    
    return ikm_admin_update_send_conf


def IKM_admin_errors_log_send() -> types.InlineKeyboardMarkup:
    """
    Подтверждение отправки ошибок из лог файла.
    :return: Клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_admin_errors_log_send = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(
        text='Прислать ошибки',
        callback_data='yes_send_errors_log')
    
    ikm_admin_errors_log_send.add(item1)
    
    return ikm_admin_errors_log_send
