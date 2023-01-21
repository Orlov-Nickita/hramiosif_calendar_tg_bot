import emoji
import telebot
from telegram import ChatAction, ParseMode

from keyboards_for_bot.admin_keyboards import IKM_admin_log_remove_conf, IKM_admin_errors_log_send
from loader import bot, administrators, log_file_name, log_dir
from utils.custom_funcs import button_text
from utils.logger import logger


def upload_logs(message: telebot.types.Message) -> None:
    """
    Функция для получения файла с логами.
    :param message: Сообщение от пользователя.
    :return: Файл с логами.
    """
    logger.info('Запущена функция admin_logs.upload_logs',
                username=message.chat.username,
                user_id=message.chat.id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
    
    bot.send_document(chat_id=message.chat.id,
                      document=open(log_dir + log_file_name, 'rb'))
    
    logger.info('Бот отправил файл с логами',
                user_id=message.chat.id)


err_count = 0
err_text = ''

def check_errors(message: telebot.types.Message) -> None:
    """
    Функция для анализа ошибок.
    :param message: Сообщение от пользователя.
    :return: Количество ошибок.
    """
    logger.info('Запущена функция admin_logs.check_errors',
                username=message.chat.username,
                user_id=message.chat.id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    global err_count
    global err_text
    err_count = 0
    err_text = ''
    
    with open(log_dir + log_file_name, 'r', encoding='utf-8') as file:

        for line in file.readlines():
            error = ' '.join(line.split('\n'))
            
            if '[error]' in error.lower():
                err_count += 1
                err_text += f'{err_count}: {error}\n\n'
                
    if err_count == 0:
        bot.send_message(chat_id=message.chat.id,
                         text=' {emoji1} Ошибок не найдено'.format(
                             emoji1=emoji.emojize(':white_check_mark:', language='alias')
                         ))
    
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=' {emoji1} Найдено ошибок {qty}'.format(qty=err_count,
                                                                      emoji1=emoji.emojize(':red_circle:',
                                                                                           language='alias')
                                                                      ),
                         reply_markup=IKM_admin_errors_log_send())
    
    logger.info('Бот отправил сообщение\n"{}"'.format(message.text),
                user_id=message.chat.id)


def remove_logs(message: telebot.types.Message) -> None:
    """
    Функция очистки файла с логами.
    :param message: Сообщение от пользователя.
    :return: Очистка файла.
    """
    logger.info('Запущена функция admin_logs.remove_logs',
                username=message.chat.username,
                user_id=message.chat.id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.FIND_LOCATION)
    
    if message.chat.id == administrators['Никита']:
        
        msg = bot.send_message(chat_id=message.chat.id,
                               text='Подтвердите удаление',
                               reply_markup=IKM_admin_log_remove_conf())
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text='У Вас нет прав доступа')
        
        bot.send_message(chat_id=administrators['Никита'],
                         text='Пользователь пытался удалить лог-файл:\n'
                              'tg_id: <code>{id}</code>\n'
                              'username: <code>{user}</code>\n'
                              'name: <code>{name}</code>\n'
                              'surname: <code>{surname}</code>\n'.format(id=message.chat.id,
                                                                         user=message.from_user.username,
                                                                         name=message.from_user.first_name,
                                                                         surname=message.from_user.last_name),
                         parse_mode=ParseMode.HTML
                         )
    
    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text),
                user_id=message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.data == 'yes_remove_log' or call.data == 'no_remove_log')
def remove_log_confirm(call: telebot.types.CallbackQuery) -> None:
    """
    Обработка нажатия на клавиатуре с подтверждением удаления лог файла
    param call: Нажатая кнопка на клавиатуре
    return: Либо происходит очистка файла, либо отмена и при условии, что это выбрал определенный пользователь
    """
    logger.info(
        'Запущена функция remove_log_confirm, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'no_remove_log':
        
        bot.send_message(chat_id=call.message.chat.id,
                         text='Удаление отменено')
        
        logger.info('Удаление отменено',
                    user_id=call.message.chat.id)
    
    else:
        
        try:
            with open(log_dir + log_file_name, 'r+') as log_file:
                log_file.truncate()
        
        except PermissionError as PerErr:
            logger.error(f'Ошибка {PerErr}',
                         user_id=call.message.chat.id)
            
            bot.send_message(chat_id=call.message.chat.id,
                             text='Лог-файл очистить не получилось')
        
        else:
            bot.send_message(chat_id=call.message.chat.id,
                             text='Лог-файл очищен')
            
            logger.info('Лог-файл очищен',
                        user_id=call.message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.data == 'yes_send_errors_log' or call.data == 'no_remove_log')
def send_errors_log(call: telebot.types.CallbackQuery) -> None:
    """
    Обработка нажатия на клавиатуре с подтверждением удаления лог файла
    param call: Нажатая кнопка на клавиатуре
    return: Либо происходит очистка файла, либо отмена и при условии, что это выбрал определенный пользователь
    """
    logger.info(
        'Запущена функция send_errors_log',
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'yes_send_errors_log':
        bot.send_message(chat_id=call.message.chat.id,
                         text=err_text)


