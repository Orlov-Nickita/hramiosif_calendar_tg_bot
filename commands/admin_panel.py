import emoji
import telebot
from telegram import ParseMode

from commands import admin_photo_week_load, admin_logs, admin_photo_month_load, __admin_hdd_check, \
    admin_upload_excel_file
from keyboards_for_bot.admin_keyboards import IKM_admin_panel_main, IKM_admin_open_menu
from loader import bot
from utils.logger import logger
from utils.custom_funcs import button_text


def start(message: telebot.types.Message) -> None:
    """
    Административная панель управления ботом.
    :param message: Принимается сообщение от пользователя.
    :return: Возвращается приветственное сообщение и открывается меню бота с клавиатурой.
    """
    logger.info('Запущена функция admin_panel.start',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text='{emoji} Панель управления {emoji}'.format(
                               emoji=emoji.emojize(':open_file_folder:',
                                                   language='alias')),
                           reply_markup=IKM_admin_panel_main(),
                           parse_mode=ParseMode.HTML)
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.data == 'upload_week_photo' and 'Панель управления' in call.message.text)
def save_schedule_to_the_week(call: telebot.types.CallbackQuery) -> None:
    logger.info(
        'Запущена функция save_schedule_to_the_week, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=IKM_admin_open_menu())
    
    admin_photo_week_load.start_week(call.message)


@bot.callback_query_handler(
    func=lambda call: call.data == 'upload_month_photo' and 'Панель управления' in call.message.text)
def save_schedule_to_the_month(call: telebot.types.CallbackQuery) -> None:
    logger.info(
        'Запущена функция save_schedule_to_the_month, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=IKM_admin_open_menu())
    
    admin_photo_month_load.start_month(call.message)


@bot.callback_query_handler(
    func=lambda call: call.data == 'upload_excel_file' and 'Панель управления' in call.message.text)
def upload_excel_file(call: telebot.types.CallbackQuery) -> None:
    logger.info(
        'Запущена функция upload_excel_file, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    admin_upload_excel_file.start(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'logs_download' and 'Панель управления' in call.message.text)
def pull_log_file(call: telebot.types.CallbackQuery) -> None:
    logger.info(
        'Запущена функция pull_log_file, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    admin_logs.upload_logs(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'logs_trash' and 'Панель управления' in call.message.text)
def remove_log_file(call: telebot.types.CallbackQuery) -> None:
    logger.info(
        'Запущена функция remove_log_file, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    admin_logs.remove_logs(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'show_hdd' and 'Панель управления' in call.message.text)
def showing_hdd(call: telebot.types.CallbackQuery) -> None:
    logger.info(
        'Запущена функция showing_hdd, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    # __admin_hdd_check.start(call.message)
    pass


@bot.callback_query_handler(func=lambda call: call.data == 'remove_hdd' and 'Панель управления' in call.message.text)
def removing_hdd(call: telebot.types.CallbackQuery) -> None:
    pass
