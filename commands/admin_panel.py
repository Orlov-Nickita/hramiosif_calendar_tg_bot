"""
Модуль обработки админ команды на открытие панели управления
"""

import emoji
import telebot
from telegram import ParseMode
from commands import admin_photo_week_load, admin_logs, admin_photo_month_load, \
    admin_upload_excel_file, admin_sql, admin_send_update_msg, admin_hdd_check, admin_send_manual
from keyboards_for_bot.admin_keyboards import IKM_admin_panel_main, IKM_admin_open_menu, IKM_admin_panel_short
from loader import bot, administrators
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
    
    if message.chat.id == administrators['Никита']:
        msg = bot.send_message(chat_id=message.chat.id,
                               text='{emoji} Панель управления {emoji}'.format(
                                   emoji=emoji.emojize(':open_file_folder:',
                                                       language='alias')),
                               reply_markup=IKM_admin_panel_main(),
                               parse_mode=ParseMode.HTML)
    
    else:
        
        msg = bot.send_message(chat_id=message.chat.id,
                               text='{emoji} Панель управления {emoji}'.format(
                                   emoji=emoji.emojize(':open_file_folder:',
                                                       language='alias')),
                               reply_markup=IKM_admin_panel_short(),
                               parse_mode=ParseMode.HTML)
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'upload_week_photo'
                                              or call.data == 'upload_month_photo'
                                              or call.data == 'upload_excel_file'
                                              or call.data == 'sql_bd_download'
                                              or call.data == 'logs_download'
                                              or call.data == 'logs_trash'
                                              or call.data == 'logs_check_errors'
                                              or call.data == 'followers'
                                              or call.data == 'send_update_message'
                                              or call.data == 'hdd_check'
                                              or call.data == 'admin_manual_download'
                                              and 'Панель управления' in call.message.text)
def admin_panels_funcs(call: telebot.types.CallbackQuery) -> None:
    logger.info(
        'Запущена функция admin_panels_funcs, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=IKM_admin_open_menu())
    
    if call.data == 'upload_week_photo':
        admin_photo_week_load.start_week(call.message)
    
    if call.data == 'upload_month_photo':
        admin_photo_month_load.start_month(call.message)
    
    if call.data == 'upload_excel_file':
        admin_upload_excel_file.start(call.message)
    
    if call.data == 'sql_bd_download':
        admin_sql.upload_sql(call.message)
    
    if call.data == 'logs_download':
        admin_logs.upload_logs(call.message)
    
    if call.data == 'logs_trash':
        admin_logs.remove_logs(call.message)
    
    if call.data == 'logs_check_errors':
        admin_logs.check_errors(call.message)
    
    if call.data == 'followers':
        admin_sql.followers_func(call.message)
    
    if call.data == 'send_update_message':
        admin_send_update_msg.start(call.message)
    
    if call.data == 'hdd_check':
        admin_hdd_check.start(call.message)

    if call.data == 'admin_manual_download':
        admin_send_manual.upload_admin_manual(call.message)


@bot.callback_query_handler(
    func=lambda call: call.data == 'open_menu_again'
                      and 'Панель управления' in call.message.text)
def open_menu_again_func(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик повторного открытия меню
    """
    logger.info(
        'Запущена функция open_menu_week, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'open_menu_again':
        if call.message.chat.id == administrators['Никита']:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='{emoji} Панель управления {emoji}'.format(
                                      emoji=emoji.emojize(':open_file_folder:',
                                                          language='alias')),
                                  reply_markup=IKM_admin_panel_main(),
                                  parse_mode=ParseMode.HTML)
        
        else:
            
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='{emoji} Панель управления {emoji}'.format(
                                      emoji=emoji.emojize(':open_file_folder:',
                                                          language='alias')),
                                  reply_markup=IKM_admin_panel_short(),
                                  parse_mode=ParseMode.HTML)
