"""
Модуль с кастомными функциями для работы других модулей
"""

import os.path
from typing import List

from aiogram.dispatcher import FSMContext

from excel_utils.open_check_funcs import check_new_file, open_to_dict, data_to_json, to_lists_of_column, \
    data_from_json, reversed_dict_days_and_row_index
from excel_utils.parsing_funcs import all_days_in_schedule_file
from loader import excel_file_name, schedules_excel_dir, json_excel_file, json_days_list, json_days_with_index, \
    json_days_with_lines, json_timing, json_saints
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup


def button_text(button_call: CallbackQuery):
    """
    Функция для определения нажатой кнопки Пользователем
    :param button_call: Параметр содержит callback_data нажатой кнопки
    :type button_call:  CallbackQuery
    :return: Возвращается текст, который написан на кнопке, чтобы определить, на какую именно кнопку нажал пользователь
    """
    
    def keyboard_buttons_unpack(inline_key: List) -> List:
        """
        Функция-рекурсия для создания одноуровневого списка из многоуровневого списка
        :param inline_key: Параметр содержит многоуровневый список всех кнопок в клавиатуре, которая содержится в
        параметре Call нажатой кнопки
        :type inline_key: List
        :return: Возвращается одноуровневый список словарей со всеми кнопками
        """
        new_list = list()
        for i in inline_key:
            if isinstance(i, list):
                new_list.extend(keyboard_buttons_unpack(i))
            else:
                new_list.append(i)
        return new_list
    
    def text_button_pressed(but_list: List, call: CallbackQuery) -> str:
        """
        Функция для нахождения нажатой кнопки
        :param but_list: Параметр содержит список словарей с кнопками
        :type but_list: List
        :param call: Параметр содержит словарь данных нажатой кнопки
        :type call: CallbackQuery
        :return: Возвращается текст нажатой кнопки
        """
        for i in but_list:
            if i['callback_data'] == call.data:
                return i['text']
    
    a = keyboard_buttons_unpack(button_call.message.reply_markup.inline_keyboard)
    return text_button_pressed(a, button_call)


async def load_photo_or_doc_from_bot(bot, logger, msg: Message, src: str,
                                     downloaded_file: bytes, bot_text: str,
                                     keyboard: InlineKeyboardMarkup = None, photo: bool = False, doc: bool = False,
                                     other_week: bool = False, state: FSMContext = None):
    """
    Функция сохранения файла. Фото или файл. Если присылается файл Excel, то программа проверяет отличие от
    текущего файла JSON и если есть отличие, то делает перезапись файлов на актуальные данные.
    param bot: Ссылка на переменную, в которой хранится токен .
    param msg: Передается сообщение, чтобы по нему определить id сообщения и чата.
    param src: Путь до файла, куда сохранить.
    param downloaded_file: Переменная для сохранения файла в байтах.
    param bot_text: Текст, который бот должен написать в ответ.
    param keyboard: Клавиатура, которая должна быть применена после ответа бота.
    param photo: Переключатель функции для работы с фото.
    param doc: Переключатель функции для работы с Excel.
    """
    logger.info('Запущена функция load_photo_or_doc_from_bot',
                username=msg.from_user.username,
                user_id=msg.chat.id)
    
    try:
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
    
    except FileNotFoundError:
        logger.error('Файл для перезаписи не найден!')
        await bot.delete_message(chat_id=msg.chat.id,
                                 message_id=msg.message_id)
        
        msg = await bot.send_message(chat_id=msg.chat.id,
                                     text='Что-то случилось и я потерял файл для перезаписи. Начните, пожалуйста, сначала')
        
        logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                    user_id=msg.chat.id)
        
        await state.finish()
    
    else:
        if photo:
            await bot.delete_message(chat_id=msg.chat.id,
                                     message_id=msg.message_id)
            
            msg_func = await bot.send_message(chat_id=msg.chat.id,
                                              text=bot_text,
                                              reply_markup=keyboard)
            logger.info('Бот отправил сообщение "{}"'.format(msg_func.text),
                        user_id=msg.chat.id)
        
        elif doc:
            if not os.path.exists(schedules_excel_dir + json_excel_file):
                data_to_json(json_file=schedules_excel_dir + json_excel_file,
                             data_dict_or_list={})
            if not await check_new_file(new_file=schedules_excel_dir + excel_file_name,
                                        filejson=schedules_excel_dir + json_excel_file,
                                        message=msg):
                opened_xl = await open_to_dict(excel_file=schedules_excel_dir + excel_file_name,
                                               message=msg)
                data_to_json(json_file=schedules_excel_dir + json_excel_file, data_dict_or_list=opened_xl)
                
                list_of_col = to_lists_of_column(data_from_json(schedules_excel_dir + json_excel_file))
                
                data_to_json(json_file=schedules_excel_dir + json_days_list, data_dict_or_list=list_of_col[0])
                data_to_json(json_file=schedules_excel_dir + json_days_with_lines,
                             data_dict_or_list=all_days_in_schedule_file(
                                 jsonfile=schedules_excel_dir + json_days_list))
                data_to_json(json_file=schedules_excel_dir + json_days_with_index,
                             data_dict_or_list=reversed_dict_days_and_row_index(data_from_json(
                                 json_file=schedules_excel_dir + json_excel_file)))
                data_to_json(json_file=schedules_excel_dir + json_saints, data_dict_or_list=list_of_col[1])
                data_to_json(json_file=schedules_excel_dir + json_timing, data_dict_or_list=list_of_col[2])
                
                if await check_new_file(new_file=schedules_excel_dir + excel_file_name,
                                        filejson=schedules_excel_dir + json_excel_file,
                                        message=msg):
                    msg_func = await bot.send_message(chat_id=msg.chat.id,
                                                      text=bot_text)
                else:
                    msg_func = await bot.send_message(chat_id=msg.chat.id,
                                                      text='Произошла ошибка')
                    await state.finish()
                    
                logger.info('Бот отправил сообщение "{}"'.format(msg_func.text),
                            user_id=msg.chat.id)
            
            else:
                msg_func = await bot.send_message(chat_id=msg.chat.id,
                                                  text='Файл точно такой же, как и у меня. Чтобы перезаписать данные, '
                                                       'нужно чтобы файл содержал хоть сколько-нибудь отличную '
                                                       'информацию от текущей')
                await state.finish()
                
                logger.info('Бот отправил сообщение "{}"'.format(msg_func.text),
                            user_id=msg.chat.id)
        
        elif other_week:
            msg_func = await bot.send_message(chat_id=msg.chat.id,
                                              text=bot_text,
                                              reply_markup=keyboard)
            logger.info('Бот отправил сообщение "{}"'.format(msg_func.text),
                        user_id=msg.chat.id)
        
        else:
            msg_func = await bot.edit_message_text(chat_id=msg.chat.id,
                                                   message_id=msg.message_id,
                                                   text=bot_text,
                                                   reply_markup=keyboard)
            logger.info('Бот отправил сообщение "{}"'.format(msg_func.text),
                        user_id=msg.chat.id)
