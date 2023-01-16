import telebot
from telegram import ChatAction, ParseMode
from loader import bot, administrators
from utils.logger import logger


def upload_logs(message: telebot.types.Message) -> None:
    """
    Функция загрузки фотографий.
    :param message: Принимается сообщение от пользователя.
    :return: Возвращается приветственное сообщение и открывается меню бота с клавиатурой.
    """
    logger.info('Запущена функция admin_logs.upload_logs',
                username=message.chat.username,
                user_id=message.chat.id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT)
    
    bot.send_document(chat_id=message.chat.id,
                      document=open('./hdd/logs/bot_detail.log', 'rb'))
    
    logger.info('Бот отправил файл с логами',
                user_id=message.chat.id)


def remove_logs(message: telebot.types.Message) -> None:
    """
    Функция загрузки фотографий.
    :param message: Принимается сообщение от пользователя.
    :return: Возвращается приветственное сообщение и открывается меню бота с клавиатурой.
    """
    logger.info('Запущена функция admin_logs.remove_logs',
                username=message.chat.username,
                user_id=message.chat.id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.FIND_LOCATION)
    
    if message.chat.id == administrators['Никита']:
        try:
            with open('./hdd/logs/bot_detail.log', 'r+') as log_file:
                log_file.truncate()
            
        except PermissionError as PerErr:
            logger.error(f'Ошибка {PerErr}',
                         user_id=message.chat.id)
            
            bot.send_message(chat_id=message.chat.id,
                             text='Лог-файл очистить не получилось')
            
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Лог-файл очищен')
    
            logger.info('Лог-файл очищен',
                        user_id=message.chat.id)
    
    else:
        bot.send_message(chat_id=message.chat.id,
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
