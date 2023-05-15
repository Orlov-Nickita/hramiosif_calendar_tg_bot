"""
Модуль обработки админ команды на загрузку недельного расписания
"""

import pytz
import os.path
import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from commands.admin_photo_month_load import start_month
from errors import FileError
from keyboards_for_bot.admin_keyboards import IKM_admin_week_save_photo, IKM_admin_save_photo_again, \
    IKM_admin_overwrite_file_first_choice, IKM_admin_overwrite_file_second_choice
from loader import bot, schedule_photo_week_dir, week_photo_name, dp
from utils.logger import logger
from utils.custom_funcs import button_text, load_photo_or_doc_from_bot
from aiogram.types import Message, ParseMode, CallbackQuery


class WeekPhotoDownload(StatesGroup):
    """
    Машина состояний
    get_file: Для процесса первичной загрузки файла
    week_choice: Для процесса выбора недели (текущий, следующий, другой)
    first_change_file: Для процесса первичной перезаписи
    second_change_file: Для процесса вторичной перезаписи (когда уточняется точно ли перезаписать)
    week_number_choice: Для выбора числа недели
    file_id: Id файла
    src: Путь записи файла
    downloaded_file: Байт-строка скачанного файла
    """
    get_file = State()
    week_choice = State()
    first_change_file = State()
    second_change_file = State()
    week_number_choice = State()
    file_id = ''
    src = ''
    downloaded_file = b''


async def start_week(message: Message) -> None:
    """
    Стартовая функция начала процесса загрузки фотографий.
    :param message: Сообщение от пользователя.
    :return: Сообщение от бота и ожидание фотографии.
    """
    logger.info('Запущена функция admin_photo_week_load.start_week',
                username=message.chat.username,
                user_id=message.chat.id)
    
    await WeekPhotoDownload.get_file.set()
    
    msg = await bot.send_message(chat_id=message.chat.id,
                                 text='Пришли расписание на неделю и я сохраню')
    
    logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                user_id=message.chat.id)


@dp.message_handler(lambda message: message.text == 'Отмена' or message.text == 'отмена',
                    state=WeekPhotoDownload)
async def cancel_upload(message: Message, state: FSMContext) -> None:
    """
    Функция обработчик отмены действий
    :param message: Сообщение от пользователя.
    :param state: Состояние машины состояний
    """
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(text='Загрузка отменена', chat_id=message.chat.id)
    await state.finish()


@dp.message_handler(content_types=['text', 'document', 'photo'], state=WeekPhotoDownload.get_file)
async def photo_week(message: Message, state: FSMContext) -> None:
    """
    Функция обработчик присланного файла
    :param message: Сообщение от пользователя.
    :param state: Состояние машины состояний
    """
    logger.info('Запущена функция photo_week пользователь отправил в бот файл',
                username=message.chat.username,
                user_id=message.chat.id)
    
    try:
        if not os.path.exists(schedule_photo_week_dir):
            os.makedirs(schedule_photo_week_dir)
        
        if message.photo:
            logger.info('Пользователь прислал фото',
                        username=message.chat.username,
                        user_id=message.chat.id)
            
            async with state.proxy() as data:
                data['get_file'] = await bot.get_file(message.photo[-1].file_id)
        
        elif message.document and 'image' in message.document.mime_type:
            
            logger.info('Пользователь прислал файл. Тип файла {}'.format(message.document.mime_type),
                        username=message.chat.username,
                        user_id=message.chat.id)
            
            async with state.proxy() as data:
                data['get_file'] = await bot.get_file(message.document.file_id)
        
        else:
            raise FileError
        
        await WeekPhotoDownload.week_choice.set()
    
    except FileError:
        logger.error('Ошибка формата файла FileError {}'.format(message),
                     username=message.from_user.username,
                     user_id=message.chat.id)
        await bot.send_message(chat_id=message.chat.id,
                               text='Ошибка. Нужно фото. Повторите отправку или отправьте команду "Отмена"')
    
    else:
        msg = await bot.send_message(text='На какую неделю это расписание?',
                                     chat_id=message.chat.id,
                                     reply_markup=IKM_admin_week_save_photo())
        
        logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                    user_id=message.chat.id)


@dp.callback_query_handler(
    lambda call: call.data in ['this_week', 'next_week', 'other_week']
                 and 'На какую неделю это расписание' in call.message.text,
    state=WeekPhotoDownload.week_choice)
async def save_photo_week(call: CallbackQuery, state: FSMContext) -> None:
    """
    Функция обработчик первой клавиатуры с определением номера неделе
    """
    logger.info(
        'Запущена функция save_photo_week, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    async with state.proxy() as data:
        temp = await bot.download_file(data['get_file'].file_path)
        data['downloaded_file'] = downloaded_file = temp.getbuffer().tobytes()
    
    if call.data == 'this_week' or call.data == 'next_week':
        if call.data == 'this_week':
            week_digit = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%U"))
        
        else:
            week_digit = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%U")) + 1
        
        try:
            async with state.proxy() as data:
                data['src'] = src = schedule_photo_week_dir + week_photo_name.format(number=week_digit)
        
        except AttributeError as AEerror:
            logger.error('Произошла ошибка {}'.format(AEerror),
                         username=call.message.from_user.username,
                         user_id=call.message.chat.id)
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Неверный формат файла, нужно фото. Повторите отправку или отправьте '
                                        'команду "Отмена"')
            
            await WeekPhotoDownload.get_file.set()
        
        else:
            if os.path.exists(src):
                msg = await bot.edit_message_text(chat_id=call.message.chat.id,
                                                  message_id=call.message.message_id,
                                                  text='Файл с расписанием на указанную неделю уже есть. Перезаписать?',
                                                  reply_markup=IKM_admin_overwrite_file_first_choice())
                
                logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                            user_id=call.message.chat.id)
                
                await WeekPhotoDownload.first_change_file.set()
            
            else:
                await load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=call.message,
                                                 src=src, downloaded_file=downloaded_file,
                                                 bot_text='Расписание на неделю загружено',
                                                 keyboard=IKM_admin_save_photo_again(), state=state)
                
                await state.finish()
    
    elif call.data == 'other_week':
        await WeekPhotoDownload.week_number_choice.set()
        
        msg = await bot.send_message(chat_id=call.message.chat.id,
                                     text='Укажите номер недели в году. Сейчас, например, идет {} неделя'.format(
                                         int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%U"))
                                     ))
        
        logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                    user_id=call.message.chat.id)


@dp.message_handler(state=WeekPhotoDownload.week_number_choice)
async def download_photo_week(message: Message, state: FSMContext) -> None:
    """
    Функция загрузки фотографии. Бот проверяет наличие и сохраняет или предлагает перезаписать
    """
    logger.info(
        'Запущена функция download_photo_week',
        username=message.from_user.username,
        user_id=message.chat.id)
    
    if message.text.isdigit():
        
        try:
            async with state.proxy() as data:
                downloaded_file = data['downloaded_file']
                data['src'] = src = schedule_photo_week_dir + week_photo_name.format(number=message.text)
        
        except AttributeError as AEerror:
            logger.error('Произошла ошибка {}'.format(AEerror),
                         username=message.from_user.username,
                         user_id=message.chat.id)
            await bot.send_message(chat_id=message.chat.id,
                                   text='Неверный формат файла, нужно фото. Повторите отправку или отправьте '
                                        'команду "Отмена"')
            
            await WeekPhotoDownload.get_file.set()
        
        else:
            if os.path.exists(src):
                msg = await bot.edit_message_text(chat_id=message.chat.id,
                                                  message_id=message.message_id,
                                                  text='Файл с расписанием на указанную неделю уже есть. Перезаписать?',
                                                  reply_markup=IKM_admin_overwrite_file_first_choice())
                
                logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                            user_id=message.chat.id)
                
                await WeekPhotoDownload.first_change_file.set()
            
            else:
                await load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=message,
                                                 src=src, downloaded_file=downloaded_file,
                                                 bot_text='Расписание на неделю загружено',
                                                 other_week=True,
                                                 keyboard=IKM_admin_save_photo_again(), state=state)
                await state.finish()
    
    else:
        msg = await bot.send_message(chat_id=message.chat.id,
                                     text='Ошибка. Нужно просто одно число или отправьте команду "Отмена"')
        logger.info('Бот написал "{}"'.format(msg.text),
                    user_id=message.chat.id)

@dp.callback_query_handler(
    lambda call: (call.data == 'yes_overwrite'
                  or call.data == 'no_overwrite')
                 and 'Файл с расписанием на указанную неделю уже есть. Перезаписать?' in call.message.text,
    state=WeekPhotoDownload.first_change_file)
async def overwrite_week(call: CallbackQuery, state: FSMContext) -> None:
    """
    Функция обработчик для перезаписи файла или проверки имеющегося в записи
    """
    logger.info(
        'Запущена функция overwrite_week, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    async with state.proxy() as data:
        downloaded_file = data['downloaded_file']
        src = data['src']
    
    if call.data == 'yes_overwrite':
        await load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=call.message,
                                         src=src, downloaded_file=downloaded_file,
                                         bot_text='Файл перезаписан, расписание на неделю загружено',
                                         keyboard=IKM_admin_save_photo_again(), state=state)
        await state.finish()
    
    elif call.data == 'no_overwrite':
        
        msg = await bot.edit_message_text(text='Файл с расписанием на указанную неделю уже есть. Перезаписать?\n'
                                               '<i>- <code>Вы выбрали {button}</code></i>'.format(
            button=button_text(call)),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode=ParseMode.HTML)
        
        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text),
                    user_id=call.message.chat.id)
        
        msg = await bot.send_photo(chat_id=call.message.chat.id,
                                   photo=open(src, 'rb'),
                                   reply_markup=IKM_admin_overwrite_file_second_choice())
        await WeekPhotoDownload.second_change_file.set()
        
        logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                    user_id=call.message.chat.id)


@dp.callback_query_handler(
    lambda call: (call.data == 'yes_overwrite_final'
                  or call.data == 'no_overwrite_final')
                 and call.message.content_type == 'photo',
    state=WeekPhotoDownload.second_change_file)
async def overwrite_week_2(call: CallbackQuery, state: FSMContext) -> None:
    """
    Функция обработчик окончательного принятия решения по перезаписи файла или отмене от операции
    """
    logger.info(
        'Запущена функция overwrite_week_2, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'yes_overwrite_final':
        async with state.proxy() as data:
            downloaded_file = data['downloaded_file']
            src = data['src']
        await load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=call.message,
                                         src=src, downloaded_file=downloaded_file,
                                         bot_text='Файл перезаписан, расписание на неделю загружено',
                                         keyboard=IKM_admin_save_photo_again(),
                                         photo=True, state=state)
        await state.finish()

    elif call.data == 'no_overwrite_final':
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
        
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Файл не перезаписан, операция отменена')
        await state.finish()


@dp.callback_query_handler(
    lambda call: call.message.content_type != 'photo'
                 and call.data == 'load_again'
                 or call.data == 'close')
async def repeat_save_photo(call: CallbackQuery) -> None:
    """
    Функция обработчик в самом последнем меню, когда предлагается выбор отправить еще фото или закрыть меню
    """
    if 'Расписание на неделю загружено' in call.message.text or \
            'Файл перезаписан, расписание на неделю загружено' in call.message.text:
        
        logger.info(
            'Запущена функция repeat_save_photo_week, пользователь нажал на кнопку "{}"'.format(button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        
        if call.data == 'load_again':
            await start_week(call.message)
        
        elif call.data == 'close':
            msg = await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                      message_id=call.message.message_id)
            
            logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                        user_id=call.message.chat.id)
    
    if 'Расписание на месяц загружено' in call.message.text or \
            'Файл перезаписан, расписание на месяц загружено' in call.message.text:
        
        logger.info(
            'Запущена функция repeat_save_photo_month, пользователь нажал на кнопку "{}"'.format(button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        
        if call.data == 'load_again':
            await start_month(call.message)
        
        elif call.data == 'close':
            msg = await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                      message_id=call.message.message_id)
            
            logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                        user_id=call.message.chat.id)
