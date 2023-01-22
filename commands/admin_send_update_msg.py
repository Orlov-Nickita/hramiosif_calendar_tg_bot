import time
import telebot
from telegram import ParseMode
from keyboards_for_bot.admin_keyboards import IKM_admin_update_send_conf
from loader import bot, users_sql_dir, users_sql_file_name, hdd_dir, update_jgp
from utils.custom_funcs import button_text
from utils.logger import logger
from utils.sql_funcs import get_info_from_sql

update_msg_text = ''


def start(message: telebot.types.Message) -> None:
    """
    Административная панель управления ботом.
    :param message: Принимается сообщение от пользователя.
    :return: Возвращается приветственное сообщение и открывается меню бота с клавиатурой.
    """
    logger.info('Запущена функция admin_send_update_msg.start',
                username=message.from_user.username,
                user_id=message.chat.id)
    
    # all_persons = get_info_from_sql(sql_base=users_sql_dir + users_sql_file_name,
    #                                 message=message)
    
    all_persons = [459901923, 434895679]
    # all_persons = [949421028]

    global update_msg_text
    update_msg_text = 'Обновление!\n' \
                      '1. Внесено изменение в формат хранимого файла для расписания на месяц. Теперь расписание на ' \
                      'месяц должно храниться в PDF\n' \
                      '2. Теперь в списке дней для вывода расписания показываются все дни начиная с текущего ' \
                      '(предыдущие не показываются)'
    
    bot.send_photo(chat_id=message.chat.id,
                   photo=open(hdd_dir + update_jgp, 'rb'),
                   caption=f'Будет отправлено {len(all_persons)} сообщений.\n'
                           f'Выглядеть будет так:\n'
                           f'\n'
                           f'{update_msg_text}\n'
                           f'\n'
                           f'Подтвердите отправку',
                   reply_markup=IKM_admin_update_send_conf())


@bot.callback_query_handler(
    func=lambda call: call.data == 'yes_send_upd_msg' or call.data == 'no_send_upd_msg')
def send_update_msg_confirm(call: telebot.types.CallbackQuery) -> None:
    """
    Обработка нажатия на клавиатуре с подтверждением отправки сообщения с обновлениями
    param call: Нажатая кнопка на клавиатуре
    return: Либо происходит очистка файла, либо отмена и при условии, что это выбрал определенный пользователь
    """
    logger.info(
        'Запущена функция send_update_msg_confirm, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    
    if call.data == 'no_send_upd_msg':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        
        bot.send_message(chat_id=call.message.chat.id,
                         text='Отправка сообщения отменена')
        
        logger.info('Отправка сообщения отменена',
                    user_id=call.message.chat.id)
    
    else:
        global update_msg_text
        
        # all_persons = get_info_from_sql(sql_base=users_sql_dir + users_sql_file_name,
        #                                 message=message)
        
        all_persons = [459901923, 434895679]
        # all_persons = [949421028]
        
        count_txt = 0
        for person in all_persons:
            time.sleep(0.5)
            print(update_msg_text)

            bot.send_photo(chat_id=person,
                           photo=open(hdd_dir + update_jgp, 'rb'),
                           caption=update_msg_text,
                           parse_mode=ParseMode.HTML)
            
            count_txt += 1
        
        logger.info('Бот разослал сообщения пользователям из базы данных {bd_list}.\n'
                    'Текст сообщения {new_msg}\n'
                    'Всего сообщений {qty_m}'.format(bd_list=all_persons,
                                                     new_msg=update_msg_text,
                                                     qty_m=count_txt),
                    user_id=call.message.chat.id)
