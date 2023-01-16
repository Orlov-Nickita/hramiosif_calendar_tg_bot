import telebot
import os.path

from keyboards_for_bot.admin_keyboards import IKM_admin_overwrite_excel_file
from loader import bot, schedules_excel_dir, excel_file_name
from utils.custom_funcs import load_photo_or_doc_from_bot, button_text
from utils.logger import logger

file_info = ''
src = ''
downloaded_file = b''
check_file_info = False


def start(message: telebot.types.Message) -> None:
    """
    .
    :param message: Принимается сообщение от пользователя.
    :return: Возвращается приветственное сообщение и открывается меню бота с клавиатурой.
    """
    logger.info('Запущена функция admin_upload_excel_file.start',
                username=message.chat.username,
                user_id=message.chat.id)
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text='Пришли файл в формате ".xlsx"')
    
    logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                user_id=message.chat.id)
    
    bot.register_next_step_handler(message=msg, callback=upload_excel_file_func)


def upload_excel_file_func(message: telebot.types.Message) -> None:
    logger.info('Запущена функция upload_excel_file_func пользователь отправил в бот файл',
                username=message.chat.username,
                user_id=message.chat.id)
    
    global file_info
    if not os.path.exists(schedules_excel_dir):
        os.makedirs(schedules_excel_dir)
    
    if os.path.splitext(bot.get_file(message.document.file_id).file_path)[1] != '.xlsx':
        logger.error('Пользователь отправил файл с неправильным форматом {}'.
                     format(os.path.splitext(bot.get_file(message.document.file_id).file_path)[1]
                            ),
                     username=message.chat.username,
                     user_id=message.chat.id)
        
        msg = bot.send_message(chat_id=message.chat.id,
                               text='Ошибка. Нужен файл в формате ".xlsx". Повторите отправку')
        
        logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                    user_id=message.chat.id)
        
        bot.register_next_step_handler(message=message, callback=upload_excel_file_func)
    
    else:
        global src
        global downloaded_file
        global check_file_info
        check_file_info = True
        
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_info.file_path = excel_file_name
        src = schedules_excel_dir + file_info.file_path
        
        if os.path.exists(src):
            msg = bot.send_message(chat_id=message.chat.id,
                                   text='Excel уже есть. Перезаписать?',
                                   reply_markup=IKM_admin_overwrite_excel_file())
            
            logger.info('Бот отправил сообщение "{}"'.format(msg.text),
                        user_id=message.chat.id)
        
        else:
            load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=message,
                                       src=src, downloaded_file=downloaded_file,
                                       bot_text='Excel сохранен', doc=True)
            
            check_file_info = False


@bot.callback_query_handler(
    func=lambda call: call.data == 'yes_overwrite_excel'
                      or call.data == 'no_leave_excel'
                      and 'Excel уже есть. Перезаписать?' in call.message.text)
def overwrite_excel_func(call: telebot.types.CallbackQuery) -> None:
    logger.info(
        'Запущена функция overwrite_excel_func, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'yes_overwrite_excel':
        global src
        global downloaded_file
        
        load_photo_or_doc_from_bot(bot=bot, logger=logger, msg=call.message,
                                   src=src, downloaded_file=downloaded_file,
                                   bot_text='Файл перезаписан, Excel сохранен',
                                   doc=True)
        global check_file_info
        check_file_info = False
    
    if call.data == 'no_leave_excel':
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text='Файл не перезаписан, операция отменена')
        
        logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text),
                    user_id=call.message.chat.id)
