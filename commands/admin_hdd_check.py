"""
Модуль обработки админ команды на просмотр жесткого диска
"""

import os
from keyboards_for_bot.admin_keyboards import IKM_admin_check_hdd, IKM_open_or_not_files_in_dir_hdd, \
    IKM_admin_in_dir_hdd_remove_conf, IKM_open_or_not_for_photo_in_dir_hdd
from loader import bot, hdd_dir, administrators, users_sql_dir, users_sql_file_name, \
    schedules_photos_dir, dp
from utils.custom_funcs import button_text
from utils.logger import logger
from utils.sql_funcs import sql_hdd_root_dir_update, sql_hdd_root_dir_get
from aiogram.types import Message, CallbackQuery


async def _get_root_hdd(msg: Message, koren: bool = False, path: bool = False) -> str:
    """
    Декоратор для получения пути директории/файла в БД
    """
    return await sql_hdd_root_dir_get(sql_base=users_sql_dir + users_sql_file_name,
                                      message=msg,
                                      koren=koren,
                                      path=path)


async def _update_root_hdd(msg: Message, direc: str, koren: bool = False, path: bool = False) -> None:
    """
    Декоратор для обновления пути директории/файла в БД
    """
    await sql_hdd_root_dir_update(sql_base=users_sql_dir + users_sql_file_name,
                                  root_dir=direc,
                                  koren=koren,
                                  path=path,
                                  message=msg)


async def _up_dir(msg: Message) -> None:
    """
    Декоратор для обновления пути директории или файла при возвращении назад
    """
    temp = await _get_root_hdd(msg=msg, path=True)
    up_dir = [i for i in temp.split('/') if i != '']
    up_dir.pop()
    up_dir = '/'.join(up_dir) + '/'
    await _update_root_hdd(msg=msg, direc=up_dir,
                           path=True)


async def what_files_in_dir(directory: str) -> list:
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


async def start(message: Message) -> None:
    """
    Функция проверки состояния жесткого диска.
    :param message: Принимается сообщение от пользователя.
    :return: Возвращается приветственное сообщение и открывается меню бота с клавиатурой.
    """
    logger.info('Запущена функция admin_hdd_check.start',
                username=message.chat.username,
                user_id=message.chat.id)
    
    if message.chat.id == int(administrators['Никита']):
        await _update_root_hdd(msg=message, direc=hdd_dir, koren=True)
        await _update_root_hdd(msg=message, direc=hdd_dir, path=True)
    
    else:
        await _update_root_hdd(msg=message, direc=schedules_photos_dir, koren=True)
        await _update_root_hdd(msg=message, direc=schedules_photos_dir, path=True)
    
    await bot.send_message(chat_id=message.chat.id,
                           text='Список файлов в папке {}'.format(''.join(
                               await _get_root_hdd(msg=message, path=True))),
                           reply_markup=IKM_admin_check_hdd(await what_files_in_dir(''.join(
                               await _get_root_hdd(msg=message, path=True)))))


@dp.callback_query_handler(lambda call: ('Папка' in button_text(call)
                                         or call.data == 'return_dir_back')
                                        and 'Список файлов' in call.message.text)
async def what_files_in_other_dir(call: CallbackQuery) -> None:
    """
    Функция обработчик нажатия на кнопку с папкой
    """
    
    logger.info(
        'Запущена функция what_files_in_other_dir, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data != 'return_dir_back':
        try:
            if not os.path.exists(await _get_root_hdd(msg=call.message, path=True)):
                raise FileNotFoundError
        
        except FileNotFoundError:
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text='Я потерял путь до директории. Начните сначала')
        
        else:
            await _update_root_hdd(msg=call.message,
                                   direc=f'{await _get_root_hdd(msg=call.message, path=True)}{call.data}/',
                                   path=True)
            if not os.path.exists(await _get_root_hdd(msg=call.message, path=True)):
                raise FileNotFoundError
            
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        text='Список файлов в папке {}'.format(''.join(
                                            await _get_root_hdd(msg=call.message, path=True)
                                        )),
                                        message_id=call.message.message_id,
                                        reply_markup=IKM_admin_check_hdd(await what_files_in_dir(''.join(
                                            await _get_root_hdd(msg=call.message, path=True)
                                        ))))
    
    else:
        if await _get_root_hdd(msg=call.message, path=True) != await _get_root_hdd(msg=call.message, koren=True):
            await _up_dir(msg=call.message)
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        text='Список файлов в папке {}'.format(''.join(
                                            await _get_root_hdd(msg=call.message, path=True)
                                        )),
                                        message_id=call.message.message_id,
                                        reply_markup=IKM_admin_check_hdd(await what_files_in_dir(''.join(
                                            await _get_root_hdd(msg=call.message, path=True)
                                        ))))
        
        else:
            msg = await bot.send_message(chat_id=call.message.chat.id,
                                         text='Это корень диска, дальше переместиться нельзя')
            
            logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                        user_id=call.message.chat.id)


@dp.callback_query_handler(lambda call: ('Файл' in button_text(call)
                                         or call.data == 'return_dir_back')
                                        and 'Список файлов' in call.message.text)
async def wth_what_the_file(call: CallbackQuery) -> None:
    """
    Функция обработчик нажатия на кнопку с файлом
    """
    
    logger.info(
        'Запущена функция wth_what_the_file, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data != 'return_dir_back':
        try:
            if not os.path.exists(await _get_root_hdd(msg=call.message, path=True)):
                raise FileNotFoundError
        
        except FileNotFoundError:
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text='Я потерял путь до директории. Начните сначала')
        
        else:
            await _update_root_hdd(msg=call.message,
                                   direc=f'{await _get_root_hdd(msg=call.message, path=True)}{call.data}',
                                   path=True)
            if not os.path.exists(await _get_root_hdd(msg=call.message, path=True)):
                raise FileNotFoundError
            
            if os.path.splitext(call.data)[1] == '.jpg' or os.path.splitext(call.data)[1] == '.png':
                await bot.delete_message(chat_id=call.message.chat.id,
                                         message_id=call.message.message_id)
                
                await bot.send_photo(chat_id=call.message.chat.id,
                                     caption='Файл {}'.format(call.data),
                                     photo=open(''.join(
                                         await _get_root_hdd(msg=call.message, path=True)
                                     ), 'rb'),
                                     reply_markup=IKM_open_or_not_for_photo_in_dir_hdd())
            
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            text='Файл {}'.format(call.data),
                                            message_id=call.message.message_id,
                                            reply_markup=IKM_open_or_not_files_in_dir_hdd())


@dp.callback_query_handler(lambda call: (call.data == 'yes_open_hdd_file'
                                         or call.data == 'no_open_hdd_file'
                                         or call.data == 'remove_hdd_file')
                           )
async def open_or_not_file_on_hdd(call: CallbackQuery) -> None:
    """
    Функция обработчик выбора действия по отношению к файлу
    """
    
    logger.info(
        'Запущена функция open_or_not_file_on_hdd, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'yes_open_hdd_file':
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
        
        await bot.send_document(chat_id=call.message.chat.id,
                                document=open(''.join(
                                    await _get_root_hdd(msg=call.message, path=True)
                                ), 'rb'))
    
    elif call.data == 'no_open_hdd_file':
        await _up_dir(msg=call.message)
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    text='Список файлов в папке {}'.format(''.join(
                                        await _get_root_hdd(msg=call.message, path=True)
                                    )),
                                    message_id=call.message.message_id,
                                    reply_markup=IKM_admin_check_hdd(await what_files_in_dir(''.join(
                                        await _get_root_hdd(msg=call.message, path=True)
                                    ))))
    
    elif call.data == 'remove_hdd_file':
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text='Подтвердите удаление',
                                    reply_markup=IKM_admin_in_dir_hdd_remove_conf())


@dp.callback_query_handler(
    lambda call: call.data == 'yes_remove_hdd_file'
                 or call.data == 'no_remove_hdd_file')
async def remove_hdd_file(call: CallbackQuery) -> None:
    """
    Функция обработчик выбора действия подтверждения удаления
    """
    
    logger.info(
        'Запущена функция remove_hdd_file, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'no_remove_hdd_file':
        await _up_dir(msg=call.message)
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    text='Список файлов в папке {}'.format(''.join(
                                        await _get_root_hdd(msg=call.message, path=True)
                                    )),
                                    message_id=call.message.message_id,
                                    reply_markup=IKM_admin_check_hdd(await what_files_in_dir(''.join(
                                        await _get_root_hdd(msg=call.message, path=True)
                                    ))))
    else:
        try:
            deleted = ''.join(
                await _get_root_hdd(msg=call.message, path=True)
            )
            os.remove(deleted)
        
        except PermissionError as PerErr:
            await bot.delete_message(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id)
            
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Удалить файл не получилось')
            
            logger.error(f'Ошибка {PerErr}',
                         user_id=call.message.chat.id)
        
        else:
            await bot.delete_message(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id)
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Файл удален')
            
            logger.warning('Пользователь удалил файл {}'.format(deleted),
                           user_id=call.message.chat.id)


@dp.callback_query_handler(lambda call: (call.data == 'return_for_photo_in_dir_hdd'
                                         or call.data == 'remove_for_photo_in_dir_hdd')
                                        and call.message.content_type == 'photo')
async def open_or_remove_for_photo_in_dir_hdd(call: CallbackQuery) -> None:
    """
    Функция обработчик выбора действия по отношению к фото
    """
    
    logger.info(
        'Запущена функция open_or_remove_for_photo_in_dir_hdd, пользователь нажал на кнопку "{}"'.format(
            button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'return_for_photo_in_dir_hdd':
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
        
        await _up_dir(msg=call.message)
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Список файлов в папке {}'.format(''.join(
                                   await _get_root_hdd(msg=call.message, path=True))),
                               reply_markup=IKM_admin_check_hdd(await what_files_in_dir(''.join(
                                   await _get_root_hdd(msg=call.message, path=True)))))
    
    if call.data == 'remove_for_photo_in_dir_hdd':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Подтвердите удаление',
                               reply_markup=IKM_admin_in_dir_hdd_remove_conf())


@dp.callback_query_handler(lambda call: call.data == 'close_hdd'
                                        and 'Список файлов' in call.message.text)
async def open_or_remove_for_photo_in_dir_hdd(call: CallbackQuery) -> None:
    """
    Функция обработчик закрытия списка файлов на HDD
    """
    if call.data == 'close_hdd':
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
