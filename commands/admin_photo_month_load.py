import pytz
import telebot
import os.path
import datetime
from telegram import ParseMode

from errors import FileError
from keyboards_for_bot.admin_keyboards import IKM_admin_save_photo_again, \
    IKM_admin_month_save_photo, IKM_admin_overwrite_file_first_choice, \
    IKM_admin_overwrite_file_second_choice
from loader import bot, schedule_photo_month_dir, month_photo_name
from utils.logger import logger
from utils.custom_funcs import button_text, load_photo_or_doc_from_bot

file_info = ''
src = ''
downloaded_file = b''
check_file_info = False


def start_month(message: telebot.types.Message) -> None:
    """
    Стартовая функция начала процесса загрузки фотографий.
    :param message: Сообщение от пользователя.
    :return: Сообщение от бота и ожидание фотографии.
    """
    logger.info('Запущена функция admin_photo_month_load.start_month',
                username=message.chat.username,
                user_id=message.chat.id)
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text='Пришли расписание на месяц и я сохраню')
    
    logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                user_id=message.chat.id)
    
    bot.register_next_step_handler(message=msg, callback=photo_month)


def photo_month(message: telebot.types.Message) -> None:
    """
    Функция обработчик присланного файла
    :param message: Сообщение от пользователя.
    """
    logger.info('Запущена функция photo_month пользователь отправил в бот файл',
                username=message.chat.username,
                user_id=message.chat.id)
    
    global file_info
    try:
        if not os.path.exists(schedule_photo_month_dir):
            os.makedirs(schedule_photo_month_dir)
        
        elif message.document and 'pdf' in message.document.mime_type:
            
            logger.info('Пользователь прислал файл. Тип файла {}'.format(message.document.mime_type),
                        username=message.chat.username,
                        user_id=message.chat.id)
            
            file_info = bot.get_file(message.document.file_id)
        
        else:
            raise FileError
        
        global check_file_info
        check_file_info = True
    
    except FileError:
        logger.error('Ошибка формата файла FileError {}'.format(message),
                     username=message.from_user.username,
                     user_id=message.chat.id)
        bot.send_message(chat_id=message.chat.id,
                         text='Ошибка. Нужен файл PDF. Повторите отправку')
    
    else:
        msg = bot.send_message(text='На какой месяц это расписание?',
                               chat_id=message.chat.id,
                               reply_markup=IKM_admin_month_save_photo())
        
        logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                    user_id=message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.data in ['this_month', 'next_month', 'other_month']
                      and check_file_info
                      and 'На какой месяц это расписание' in call.message.text)
def save_photo_month(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик первой клавиатуры с определением номера месяца
    """
    logger.info(
        'Запущена функция save_photo_month, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
    
    if call.data == 'this_month' or call.data == 'next_month':
        if call.data == 'this_month':
            month_digit = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%m"))
        
        if call.data == 'next_month':
            month_digit = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%m")) + 1
        
        global src
        global downloaded_file
        
        try:
            downloaded_file = bot.download_file(file_info.file_path)
            file_info.file_path = month_photo_name.format(number=month_digit)
            
            src = schedule_photo_month_dir + file_info.file_path
        
        except AttributeError as AEerror:
            logger.error('Произошла ошибка {}'.format(AEerror),
                         username=call.message.from_user.username,
                         user_id=call.message.chat.id)
            bot.send_message(chat_id=call.message.chat.id,
                             text='Неверный формат файла, нужен файл PDF. Повторите отправку')
            
            bot.register_next_step_handler(message=call.message, callback=photo_month)
        
        else:
            if os.path.exists(src):
                msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text='Файл с расписанием на указанный месяц уже есть. Перезаписать?',
                                            reply_markup=IKM_admin_overwrite_file_first_choice())
                
                logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                            user_id=call.message.chat.id)
            
            else:
                load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=call.message,
                                           src=src, downloaded_file=downloaded_file,
                                           bot_text='Расписание на месяц загружено',
                                           keyboard=IKM_admin_save_photo_again())
                
                global check_file_info
                check_file_info = False
    
    elif call.data == 'other_month':
        msg = bot.send_message(chat_id=call.message.chat.id,
                               text='Укажите номер месяца в году. Сейчас, например, идет {} месяц'.format(
                                   int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%m"))
                               ))
        
        logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                    user_id=call.message.chat.id)
        
        bot.register_next_step_handler(message=msg, callback=download_photo_month)


def download_photo_month(message: telebot.types.Message) -> None:
    """
    Функция загрузки фотографии. Бот проверяет наличие и сохраняет или предлагает перезаписать
    """
    logger.info(
        'Запущена функция download_photo_month',
        username=message.from_user.username,
        user_id=message.chat.id)
    
    if message.text.isdigit():
        
        global src
        global downloaded_file
        
        try:
            downloaded_file = bot.download_file(file_info.file_path)
            file_info.file_path = month_photo_name.format(number=message.text)
            
            src = schedule_photo_month_dir + file_info.file_path
        
        except AttributeError as AEerror:
            logger.error('Произошла ошибка {}'.format(AEerror),
                         username=message.from_user.username,
                         user_id=message.chat.id)
            bot.send_message(chat_id=message.chat.id,
                             text='Неверный формат файла, нужен файл PDF. Повторите отправку')
            
            bot.register_next_step_handler(message=message, callback=photo_month)
        
        else:
            if os.path.exists(src):
                msg = bot.edit_message_text(chat_id=message.chat.id,
                                            message_id=message.message_id,
                                            text='Файл с расписанием на указанный месяц уже есть. Перезаписать?',
                                            reply_markup=IKM_admin_overwrite_file_first_choice())
                
                logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                            user_id=message.chat.id)
            
            else:
                load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=message,
                                           src=src, downloaded_file=downloaded_file,
                                           bot_text='Расписание на месяц загружено',
                                           other_week=True,
                                           keyboard=IKM_admin_save_photo_again())
                global check_file_info
                check_file_info = False
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text='Ошибка. Нужно просто одно число')
        bot.register_next_step_handler(message=msg, callback=download_photo_month)


@bot.callback_query_handler(
    func=lambda call: (call.data == 'yes_overwrite'
                      or call.data == 'no_overwrite')
                      and 'Файл с расписанием на указанный месяц уже есть. Перезаписать?' in call.message.text)
def overwrite_month(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик для перезаписи файла или проверки имеющегося в записи
    """
    logger.info(
        'Запущена функция overwrite_month, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'yes_overwrite':
        global src
        global downloaded_file
        
        load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=call.message,
                                   src=src, downloaded_file=downloaded_file,
                                   bot_text='Файл перезаписан, расписание на месяц загружено',
                                   keyboard=IKM_admin_save_photo_again())
        global check_file_info
        check_file_info = False
    
    elif call.data == 'no_overwrite':
        
        msg = bot.edit_message_text(text='Файл с расписанием на указанный месяц уже есть. Перезаписать?\n'
                                         '<i>- <code>Вы выбрали {button}</code></i>'.format(
            button=button_text(call)),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode=ParseMode.HTML)
        
        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text),
                    user_id=call.message.chat.id)
        
        msg = bot.send_document(chat_id=call.message.chat.id,
                                document=open(src, 'rb'),
                                reply_markup=IKM_admin_overwrite_file_second_choice())
        
        logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                    user_id=call.message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.data == 'yes_overwrite_final'
                      or call.data == 'no_overwrite_final'
                      and call.message.content_type == 'photo')
def overwrite_month_2(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик окончательного принятия решения по перезаписи файла или отмене от операции
    """
    logger.info(
        'Запущена функция overwrite_month_2, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'yes_overwrite_final':
        global src
        global downloaded_file
        
        load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=call.message,
                                   src=src, downloaded_file=downloaded_file,
                                   bot_text='Файл перезаписан, расписание на месяц загружено',
                                   keyboard=IKM_admin_save_photo_again(),
                                   photo=True)
        global check_file_info
        check_file_info = False
    
    elif call.data == 'no_overwrite_final':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        
        bot.send_message(chat_id=call.message.chat.id,
                         text='Файл не перезаписан, операция отменена')
