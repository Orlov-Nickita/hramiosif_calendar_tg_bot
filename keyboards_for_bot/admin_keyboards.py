"""
Модуль с клавиатурами для панели управления со стороны администраторов
"""

import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def IKM_admin_panel_short() -> InlineKeyboardMarkup:
    """
    Клавиатура для панели управления с определенными действиями.
    :return: Возвращается клавиатура.
    """
    ikm_admin_panel_short = InlineKeyboardMarkup(row_width=1)

    btn1 = InlineKeyboardButton(
        text='{emoji} JPG|PNG фото расписания на неделю'.format(
            emoji=emoji.emojize(':camera:',
                                language='alias')),
        callback_data='upload_week_photo')

    btn2 = InlineKeyboardButton(
        text='{emoji} PDF файл расписания на месяц'.format(
            emoji=emoji.emojize(':scroll:',
                                language='alias')),
        callback_data='upload_month_photo')

    btn3 = InlineKeyboardButton(
        text='{emoji} Excel файл расписания на месяц'.format(
            emoji=emoji.emojize(':bookmark_tabs:',
                                language='alias')),
        callback_data='upload_excel_file')

    btn4 = InlineKeyboardButton(
        text='{emoji} Подписчики'.format(
            emoji=emoji.emojize(':restroom:',
                                language='alias')),
        callback_data='followers')

    btn5 = InlineKeyboardButton(
        text='{emoji} Посмотреть жесткий диск'.format(
            emoji=emoji.emojize(':floppy_disk:',
                                language='alias')),
        callback_data='hdd_check')

    btn6 = InlineKeyboardButton(
        text='{emoji} Руководство пользователя для администратора'.format(
            emoji=emoji.emojize(':magnifying_glass_tilted_left:',
                                language='alias')),
        callback_data='admin_manual_download')

    ikm_admin_panel_short.add(btn1, btn2, btn3, btn4, btn5, btn6)

    return ikm_admin_panel_short


def IKM_admin_panel_main() -> InlineKeyboardMarkup:
    """
    Клавиатура для панели управления со всеми функциями для главного администратора.
    :return: Возвращается клавиатура.
    """
    ikm_admin_panel_main = InlineKeyboardMarkup(row_width=1)

    btn1 = InlineKeyboardButton(
        text='{emoji} JPG|PNG фото расписания на неделю'.format(
            emoji=emoji.emojize(':camera:',
                                language='alias')),
        callback_data='upload_week_photo')

    btn2 = InlineKeyboardButton(
        text='{emoji} PDF файл расписания на месяц'.format(
            emoji=emoji.emojize(':scroll:',
                                language='alias')),
        callback_data='upload_month_photo')

    btn3 = InlineKeyboardButton(
        text='{emoji} Excel файл расписания на месяц'.format(
            emoji=emoji.emojize(':bookmark_tabs:',
                                language='alias')),
        callback_data='upload_excel_file')

    btn4 = InlineKeyboardButton(
        text='{emoji} Прислать файл БД'.format(
            emoji=emoji.emojize(':passport_control:',
                                language='alias')),
        callback_data='sql_bd_download')

    btn5 = InlineKeyboardButton(
        text='{emoji} Проверить ошибки лог-файла'.format(
            emoji=emoji.emojize(':interrobang:',
                                language='alias')),
        callback_data='logs_check_errors')

    btn6 = InlineKeyboardButton(
        text='{emoji} Прислать лог-файл'.format(
            emoji=emoji.emojize(':blue_book:',
                                language='alias')),
        callback_data='logs_download')

    btn7 = InlineKeyboardButton(
        text='{emoji} Очистить лог-файл'.format(
            emoji=emoji.emojize(':recycle:',
                                language='alias')),
        callback_data='logs_trash')

    btn8 = InlineKeyboardButton(
        text='{emoji} Подписчики'.format(
            emoji=emoji.emojize(':restroom:',
                                language='alias')),
        callback_data='followers')

    btn9 = InlineKeyboardButton(
        text='{emoji} Сообщить об обновлениях'.format(
            emoji=emoji.emojize(':boom:',
                                language='alias')),
        callback_data='send_update_message')

    btn10 = InlineKeyboardButton(
        text='{emoji} Посмотреть жесткий диск'.format(
            emoji=emoji.emojize(':floppy_disk:',
                                language='alias')),
        callback_data='hdd_check')

    btn11 = InlineKeyboardButton(
        text='{emoji} Руководство пользователя для администратора'.format(
            emoji=emoji.emojize(':magnifying_glass_tilted_left:',
                                language='alias')),
        callback_data='admin_manual_download')

    ikm_admin_panel_main.add(btn1, btn2, btn3, btn4,
                             btn5, btn6, btn7, btn8,
                             btn9, btn10, btn11)

    return ikm_admin_panel_main


def IKM_admin_week_save_photo() -> InlineKeyboardMarkup:
    """
    Клавиатура для присвоения названия для фото для недельного расписания.
    :return: Возвращается клавиатура.
    """
    ikm_admin_week_save_photo = InlineKeyboardMarkup(row_width=2)

    btn1 = InlineKeyboardButton(text='Текущая', callback_data='this_week')
    btn2 = InlineKeyboardButton(text='Следующая', callback_data='next_week')
    btn3 = InlineKeyboardButton(text='Другая неделя', callback_data='other_week')

    ikm_admin_week_save_photo.add(btn1, btn2, btn3)

    return ikm_admin_week_save_photo


def IKM_admin_month_save_photo() -> InlineKeyboardMarkup:
    """
    Клавиатура для присвоения названия для фото.
    :return: Возвращается клавиатура.
    """
    ikm_admin_month_save_photo = InlineKeyboardMarkup(row_width=2)

    btn1 = InlineKeyboardButton(text='Текущий', callback_data='this_month')
    btn2 = InlineKeyboardButton(text='Следующий', callback_data='next_month')
    btn3 = InlineKeyboardButton(text='Другой месяц', callback_data='other_month')

    ikm_admin_month_save_photo.add(btn1, btn2, btn3)

    return ikm_admin_month_save_photo


def IKM_admin_save_photo_again() -> InlineKeyboardMarkup:
    """
    Отправить еще фото или закрыть меню для месячного расписания.
    :return: Возвращается клавиатура.
    """
    ikm_admin_save_photo_again = InlineKeyboardMarkup(row_width=2)

    btn1 = InlineKeyboardButton(text='Отправить еще', callback_data='load_again')
    btn2 = InlineKeyboardButton(text='Закрыть меню', callback_data='close')

    ikm_admin_save_photo_again.add(btn1, btn2)

    return ikm_admin_save_photo_again


def IKM_admin_overwrite_file_first_choice() -> InlineKeyboardMarkup:
    """
    Клавиатура с возможностью оценить перезаписываемый файл.
    :return: Возвращается клавиатура.
    """
    ikm_admin_overwrite_file_first_choice = InlineKeyboardMarkup(row_width=1)

    btn1 = InlineKeyboardButton(text='Перезаписать', callback_data='yes_overwrite')
    btn2 = InlineKeyboardButton(text='Нет, посмотреть файл перед удалением', callback_data='no_overwrite')

    ikm_admin_overwrite_file_first_choice.add(btn1, btn2)

    return ikm_admin_overwrite_file_first_choice


def IKM_admin_overwrite_file_second_choice() -> InlineKeyboardMarkup:
    """
    Клавиатура с возможностью перезаписать или оставить имеющийся файл.
    :return: Возвращается клавиатура.
    """
    ikm_admin_overwrite_file_second_choice = InlineKeyboardMarkup(row_width=1)

    btn1 = InlineKeyboardButton(text='Да, перезаписать', callback_data='yes_overwrite_final')
    btn2 = InlineKeyboardButton(text='Нет, оставить', callback_data='no_overwrite_final')

    ikm_admin_overwrite_file_second_choice.add(btn1, btn2)

    return ikm_admin_overwrite_file_second_choice


def IKM_admin_overwrite_excel_file() -> InlineKeyboardMarkup:
    """
    Клавиатура с возможностью перезаписать или оставить имеющийся файл Excel.
    :return: Возвращается клавиатура.
    """
    ikm_admin_overwrite_excel_file = InlineKeyboardMarkup(row_width=1)

    btn1 = InlineKeyboardButton(text='Да, перезаписать', callback_data='yes_overwrite_excel')
    btn2 = InlineKeyboardButton(text='Нет, оставить', callback_data='no_leave_excel')

    ikm_admin_overwrite_excel_file.add(btn1, btn2)

    return ikm_admin_overwrite_excel_file


def IKM_admin_check_hdd(files: list) -> InlineKeyboardMarkup:
    """
    Меню управления файловой системой на жестком диске.
    :return: Возвращается клавиатура.
    """
    ikm_admin_check_hdd = InlineKeyboardMarkup(row_width=1)

    for file in files:
        if file[0] == 'Папка':
            ikm_admin_check_hdd.add(InlineKeyboardButton(
                text='{} {} {}'.format(emoji.emojize(':file_folder:', language='alias'),
                                       file[0],
                                       file[1]),
                callback_data=file[1])
            )

        if file[0] == 'Файл':
            ikm_admin_check_hdd.add(InlineKeyboardButton(
                text='{} {} {}'.format(emoji.emojize(':book:', language='alias'),
                                       file[0],
                                       file[1]),
                callback_data=file[1])
            )

    ikm_admin_check_hdd.add(InlineKeyboardButton(text='{emoji} Вернуться назад {emoji}'.format(
        emoji=emoji.emojize(':back:',
                            language='alias')),
        callback_data='return_dir_back'))

    ikm_admin_check_hdd.add(InlineKeyboardButton(text='{emoji} Закрыть меню {emoji}'.format(
        emoji=emoji.emojize(':x:',
                            language='alias')),
        callback_data='close_hdd'))

    return ikm_admin_check_hdd


def IKM_open_or_not_files_in_dir_hdd() -> InlineKeyboardMarkup:
    """
    Меню управления для выбора действий с файлом
    """
    ikm_open_or_not_files_in_dir_hdd = InlineKeyboardMarkup(row_width=2)

    btn1 = InlineKeyboardButton(text='Посмотреть', callback_data='yes_open_hdd_file')
    btn2 = InlineKeyboardButton(text='Назад', callback_data='no_open_hdd_file')
    btn3 = InlineKeyboardButton(text='Удалить файл', callback_data='remove_hdd_file')

    ikm_open_or_not_files_in_dir_hdd.add(btn1, btn2, btn3)

    return ikm_open_or_not_files_in_dir_hdd


def IKM_open_or_not_for_photo_in_dir_hdd() -> InlineKeyboardMarkup:
    """
    Меню управления для выбора действий с фотографией, потому что фотография открывается в предпросмотр, а
    файл можно только принудительно вызвать
    """
    ikm_open_or_not_for_photo_in_dir_hdd = InlineKeyboardMarkup(row_width=2)

    btn1 = InlineKeyboardButton(text='Назад', callback_data='return_for_photo_in_dir_hdd')
    btn2 = InlineKeyboardButton(text='Удалить', callback_data='remove_for_photo_in_dir_hdd')

    ikm_open_or_not_for_photo_in_dir_hdd.add(btn1, btn2)

    return ikm_open_or_not_for_photo_in_dir_hdd


def IKM_admin_in_dir_hdd_remove_conf() -> InlineKeyboardMarkup:
    """
    Подтверждение очистки лог файла.
    :return: Клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_admin_in_dir_hdd_remove_conf = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(
        text='Удалить',
        callback_data='yes_remove_hdd_file')

    item2 = InlineKeyboardButton(
        text='Нет',
        callback_data='no_remove_hdd_file')

    ikm_admin_in_dir_hdd_remove_conf.add(item1, item2)

    return ikm_admin_in_dir_hdd_remove_conf


def IKM_admin_open_menu() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой "Открыть меню" для открытия панели управления
    :return:
    """
    ikm_admin_open_menu = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Открыть меню',
                                                                          callback_data='open_menu_again'))

    return ikm_admin_open_menu


def IKM_admin_log_remove_conf() -> InlineKeyboardMarkup:
    """
    Подтверждение очистки лог файла.
    :return: Клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_admin_log_remove_conf = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(
        text='Удалить',
        callback_data='yes_remove_log')

    item2 = InlineKeyboardButton(
        text='Нет',
        callback_data='no_remove_log')

    ikm_admin_log_remove_conf.add(item1, item2)

    return ikm_admin_log_remove_conf


def IKM_admin_update_send_conf() -> InlineKeyboardMarkup:
    """
    Подтверждение отправки сообщений с обновлениями.
    :return: Клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_admin_update_send_conf = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(
        text='Да',
        callback_data='yes_send_upd_msg')

    item2 = InlineKeyboardButton(
        text='Нет',
        callback_data='no_send_upd_msg')

    ikm_admin_update_send_conf.add(item1, item2)

    return ikm_admin_update_send_conf


def IKM_admin_errors_log_send() -> InlineKeyboardMarkup:
    """
    Подтверждение отправки ошибок из лог-файла.
    :return: Клавиатура (функция) как объект.
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_admin_errors_log_send = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(
        text='Прислать ошибки',
        callback_data='yes_send_errors_log')

    ikm_admin_errors_log_send.add(item1)

    return ikm_admin_errors_log_send


def IKM_month_qty_questions(month_list_with_qty_ques: list) -> InlineKeyboardMarkup:
    """
    TODO
    """
    ikm_month_qty_questions = InlineKeyboardMarkup(row_width=2)

    for line in month_list_with_qty_ques:
        ikm_month_qty_questions.add(InlineKeyboardButton(text=f'{line[0]} - {line[1]} вопросов',
                                                         callback_data=line[0]))

    # ikm_month_qty_questions.add(InlineKeyboardButton(text='Вернуться назад',
    #                                                  callback_data='return'))

    return ikm_month_qty_questions
