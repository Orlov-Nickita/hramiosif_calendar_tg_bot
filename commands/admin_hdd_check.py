"""
Модуль обработки админ команды на просмотр жесткого диска
"""

from typing import List
import telebot
import os
from keyboards_for_bot.admin_keyboards import IKM_admin_check_hdd, IKM_open_or_not_files_in_dir_hdd, \
    IKM_admin_in_dir_hdd_remove_conf, IKM_open_or_not_for_photo_in_dir_hdd
from loader import bot, hdd_dir, administrators, users_sql_dir, users_sql_file_name, \
    schedules_photos_dir
from utils.custom_funcs import button_text
from utils.logger import logger
from utils.sql_funcs import sql_hdd_root_dir_update, sql_hdd_root_dir_get


def _get_root_hdd(msg, koren: bool = False, path: bool = False):
    """
    Декоратор для получения пути директории/файла в БД
    """
    return sql_hdd_root_dir_get(sql_base=users_sql_dir + users_sql_file_name,
                                message=msg,
                                koren=koren,
                                path=path)


def _update_root_hdd(msg, direc, koren: bool = False, path: bool = False):
    """
    Декоратор для обновления пути директории/файла в БД
    """
    sql_hdd_root_dir_update(sql_base=users_sql_dir + users_sql_file_name,
                            root_dir=direc,
                            koren=koren,
                            path=path,
                            message=msg)


def _up_dir(msg):
    """
    Декоратор для обновления пути директории или файла при возвращении назад
    """
    up_dir = [i for i in _get_root_hdd(msg=msg, path=True).split('/') if i != '']
    up_dir.pop()
    up_dir = '/'.join(up_dir) + '/'
    _update_root_hdd(msg=msg, direc=up_dir,
                     path=True)


def what_files_in_dir(directory: str) -> List:
    """
    Функция, которая выдает список файлов и папок в текущей директории
    param directory: путь к папке
    """
    files = []
    
    for i in os.listdir(directory):
        if i.startswith('__') or i.startswith('.'):
            continue
        elif not os.path.splitext(i)[1]:
            files.append(('Папка', i))
        else:
            files.append(('Файл', i))
    
    return files


def start(message: telebot.types.Message) -> None:
    """
    Функция проверки состояния жесткого диска.
    :param message: Принимается сообщение от пользователя.
    :return: Возвращается приветственное сообщение и открывается меню бота с клавиатурой.
    """
    logger.info('Запущена функция admin_hdd_check.start',
                username=message.chat.username,
                user_id=message.chat.id)
    
    if message.chat.id == administrators['Никита']:
        _update_root_hdd(msg=message, direc=hdd_dir, koren=True)
        _update_root_hdd(msg=message, direc=hdd_dir, path=True)
    
    else:
        _update_root_hdd(msg=message, direc=schedules_photos_dir, koren=True)
        _update_root_hdd(msg=message, direc=schedules_photos_dir, path=True)
    
    bot.send_message(chat_id=message.chat.id,
                     text='Список файлов в папке {}'.format(''.join(
                         _get_root_hdd(msg=message, path=True)
                     )),
                     reply_markup=IKM_admin_check_hdd(what_files_in_dir(''.join(
                         _get_root_hdd(msg=message, path=True)
                     ))))


@bot.callback_query_handler(func=lambda call: ('Папка' in button_text(call)
                                               or call.data == 'return_dir_back')
                                              and 'Список файлов' in call.message.text)
def what_files_in_other_dir(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик нажатия на кнопку с папкой
    """
    
    logger.info(
        'Запущена функция what_files_in_other_dir, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data != 'return_dir_back':
        try:
            if not os.path.exists(_get_root_hdd(msg=call.message, path=True)):
                raise FileNotFoundError
        
        except FileNotFoundError:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Я потерял путь до директории. Начните сначала')
        
        else:
            _update_root_hdd(msg=call.message, direc=f'{_get_root_hdd(msg=call.message, path=True)}{call.data}/',
                             path=True)
            if not os.path.exists(_get_root_hdd(msg=call.message, path=True)):
                raise FileNotFoundError
            
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  text='Список файлов в папке {}'.format(''.join(
                                      _get_root_hdd(msg=call.message, path=True)
                                  )),
                                  message_id=call.message.message_id,
                                  reply_markup=IKM_admin_check_hdd(what_files_in_dir(''.join(
                                      _get_root_hdd(msg=call.message, path=True)
                                  ))))
    
    else:
        if _get_root_hdd(msg=call.message, path=True) != _get_root_hdd(msg=call.message, koren=True):
            _up_dir(msg=call.message)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  text='Список файлов в папке {}'.format(''.join(
                                      _get_root_hdd(msg=call.message, path=True)
                                  )),
                                  message_id=call.message.message_id,
                                  reply_markup=IKM_admin_check_hdd(what_files_in_dir(''.join(
                                      _get_root_hdd(msg=call.message, path=True)
                                  ))))
        
        else:
            msg = bot.send_message(chat_id=call.message.chat.id,
                                   text='Это корень диска, дальше переместиться нельзя')
            
            logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                        user_id=call.message.chat.id)


@bot.callback_query_handler(func=lambda call: ('Файл' in button_text(call)
                                               or call.data == 'return_dir_back')
                                              and 'Список файлов' in call.message.text)
def wth_what_the_file(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик нажатия на кнопку с файлом
    """
    
    logger.info(
        'Запущена функция wth_what_the_file, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data != 'return_dir_back':
        try:
            if not os.path.exists(_get_root_hdd(msg=call.message, path=True)):
                raise FileNotFoundError
        
        except FileNotFoundError:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Я потерял путь до директории. Начните сначала')
        
        else:
            _update_root_hdd(msg=call.message, direc=f'{_get_root_hdd(msg=call.message, path=True)}{call.data}',
                             path=True)
            if not os.path.exists(_get_root_hdd(msg=call.message, path=True)):
                raise FileNotFoundError
            
            if os.path.splitext(call.data)[1] == '.jpg' or os.path.splitext(call.data)[1] == '.png':
                bot.delete_message(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id)
                
                bot.send_photo(chat_id=call.message.chat.id,
                               caption='Файл {}'.format(call.data),
                               photo=open(''.join(
                                   _get_root_hdd(msg=call.message, path=True)
                               ), 'rb'),
                               reply_markup=IKM_open_or_not_for_photo_in_dir_hdd())
            
            else:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      text='Файл {}'.format(call.data),
                                      message_id=call.message.message_id,
                                      reply_markup=IKM_open_or_not_files_in_dir_hdd())


@bot.callback_query_handler(func=lambda call: (call.data == 'yes_open_hdd_file'
                                               or call.data == 'no_open_hdd_file'
                                               or call.data == 'remove_hdd_file')
                            )
def open_or_not_file_on_hdd(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик выбора действия по отношению к файлу
    """
    
    logger.info(
        'Запущена функция open_or_not_file_on_hdd, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'yes_open_hdd_file':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        
        bot.send_document(chat_id=call.message.chat.id,
                          document=open(''.join(
                              _get_root_hdd(msg=call.message, path=True)
                          ), 'rb'))
    
    elif call.data == 'no_open_hdd_file':
        _up_dir(msg=call.message)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text='Список файлов в папке {}'.format(''.join(
                                  _get_root_hdd(msg=call.message, path=True)
                              )),
                              message_id=call.message.message_id,
                              reply_markup=IKM_admin_check_hdd(what_files_in_dir(''.join(
                                  _get_root_hdd(msg=call.message, path=True)
                              ))))
    
    elif call.data == 'remove_hdd_file':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Подтвердите удаление',
                              reply_markup=IKM_admin_in_dir_hdd_remove_conf())


@bot.callback_query_handler(
    func=lambda call: call.data == 'yes_remove_hdd_file'
                      or call.data == 'no_remove_hdd_file')
def remove_hdd_file(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик выбора действия подтверждения удаления
    """
    
    logger.info(
        'Запущена функция remove_hdd_file, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'no_remove_hdd_file':
        _up_dir(msg=call.message)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text='Список файлов в папке {}'.format(''.join(
                                  _get_root_hdd(msg=call.message, path=True)
                              )),
                              message_id=call.message.message_id,
                              reply_markup=IKM_admin_check_hdd(what_files_in_dir(''.join(
                                  _get_root_hdd(msg=call.message, path=True)
                              ))))
    else:
        try:
            deleted = ''.join(
                _get_root_hdd(msg=call.message, path=True)
            )
            os.remove(deleted)
        
        except PermissionError as PerErr:
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            
            bot.send_message(chat_id=call.message.chat.id,
                             text='Удалить файл не получилось')
            
            logger.error(f'Ошибка {PerErr}',
                         user_id=call.message.chat.id)
        
        else:
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id,
                             text='Файл удален')
            
            logger.warning('Пользователь удалил файл {}'.format(deleted),
                           user_id=call.message.chat.id)


@bot.callback_query_handler(func=lambda call: (call.data == 'return_for_photo_in_dir_hdd'
                                               or call.data == 'remove_for_photo_in_dir_hdd')
                                              and call.message.content_type == 'photo')
def open_or_remove_for_photo_in_dir_hdd(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик выбора действия по отношению к фото
    """
    
    logger.info(
        'Запущена функция open_or_remove_for_photo_in_dir_hdd, пользователь нажал на кнопку "{}"'.format(
            button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'return_for_photo_in_dir_hdd':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        
        _up_dir(msg=call.message)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Список файлов в папке {}'.format(''.join(
                             _get_root_hdd(msg=call.message, path=True)
                         )),
                         reply_markup=IKM_admin_check_hdd(what_files_in_dir(''.join(
                             _get_root_hdd(msg=call.message, path=True)
                         ))))
    
    if call.data == 'remove_for_photo_in_dir_hdd':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Подтвердите удаление',
                         reply_markup=IKM_admin_in_dir_hdd_remove_conf())


@bot.callback_query_handler(func=lambda call: call.data == 'close_hdd'
                                              and 'Список файлов' in call.message.text)
def open_or_remove_for_photo_in_dir_hdd(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик закрытия списка файлов на HDD
    """
    if call.data == 'close_hdd':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
