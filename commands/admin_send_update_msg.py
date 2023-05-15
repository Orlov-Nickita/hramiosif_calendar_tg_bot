"""
Модуль обработки админ команды на отправку сообщения с обновлениями
"""

import time
from aiogram.types import Message, ParseMode, CallbackQuery

from keyboards_for_bot.admin_keyboards import IKM_admin_update_send_conf
from loader import bot, hdd_dir, update_jgp, admin_manual_name, admin_manual_dir, administrators, info_jgp, \
    users_sql_dir, users_sql_file_name, dp
from loader import users_sql_dir, users_sql_file_name
from utils.custom_funcs import button_text
from utils.logger import logger
from utils.sql_funcs import get_info_from_sql_for_followers

update_msg_text = ''


async def start(message: Message) -> None:
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
    
    # all_persons = [459901923, 434895679, 949421028]
    # all_persons = [949421028]
    
    # global update_msg_text
    # update_msg_text = 'Уважаемые пользователи,\n' \
    #                   '\n' \
    #                   'Мы видим, что Вы запрашиваете расписание, но, к сожалению, мы еще не получили расписание от ' \
    #                   'настоятеля Храма. Приносим свои извинения, уведомим Вас, когда расписание станет доступным'
    #
    # bot.send_photo(chat_id=message.chat.id,
    #                photo=open(hdd_dir + update_jgp, 'rb'),
    #                caption=f'Будет отправлено {len(all_persons)} сообщений.\n'
    #                        f'Выглядеть будет так:\n'
    #                        f'\n'
    #                        f'{update_msg_text}\n'
    #                        f'\n'
    #                        f'Подтвердите отправку',
    #                reply_markup=IKM_admin_update_send_conf())
    if message.chat.id == int(administrators['Никита']):
        msg = bot.send_message(chat_id=message.chat.id,
                               text='Что отправим?')
        
        bot.register_next_step_handler(message=msg, callback=preparation_before_send)


async def preparation_before_send(message: Message) -> None:
    logger.info(
        'Запущена функция preparation_before_send',
        username=message.from_user.username,
        user_id=message.chat.id)
    
    global update_msg_text
    update_msg_text = message.text
    
    await bot.send_photo(chat_id=message.chat.id,
                         # photo=open(hdd_dir + update_jgp, 'rb'),
                         photo=open(hdd_dir + info_jgp, 'rb'),
                         caption=update_msg_text,
                         reply_markup=IKM_admin_update_send_conf())


@dp.callback_query_handler(
    lambda call: call.data == 'yes_send_upd_msg' or call.data == 'no_send_upd_msg')
async def send_update_msg_confirm(call: CallbackQuery) -> None:
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
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
        
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Отправка сообщения отменена')
        
        logger.info('Отправка сообщения отменена',
                    user_id=call.message.chat.id)
    
    else:
        global update_msg_text
        
        # all_persons = get_info_from_sql_for_followers(sql_base=users_sql_dir + users_sql_file_name,
        #                                               message=call.message)
        
        # print(get_info_from_sql_for_followers(sql_base=users_sql_dir + users_sql_file_name,
        #                                               message=call.message))
        
        # all_persons = [459901923, 434895679, 949421028]
        # all_persons = [949421028, 5022408096, 12444114124412421412]
        all_persons = [(949421028,), (5022408096,)]
        # all_persons = [(5022408096,), (1201283009,), (1765957161,), (345707936,), (1692880786,)]
        
        count_txt = 0
        not_found = []
        not_send = []
        for person in all_persons:
            time.sleep(0.5)
            
            try:
                await bot.send_photo(chat_id=person[0],
                                     # photo=open(hdd_dir + update_jgp, 'rb'),
                                     photo=open(hdd_dir + info_jgp, 'rb'),
                                     caption=update_msg_text,
                                     parse_mode=ParseMode.HTML)
                count_txt += 1
                
                logger.info('Сообщение № {}.\n'
                            'Отправлено пользователю {}'.format(count_txt,
                                                                person[0]),
                            user_id=call.message.chat.id)
            
            # except telebot.apihelper.ApiTelegramException:
            #     not_found.append(person[0])
            #     count_txt += 1
            #
            #     logger.info('Сообщение № {}.\n'
            #                 'Пользователь {} не найден'.format(count_txt,
            #                                                    person[0]),
            #                 user_id=call.message.chat.id)
            #     continue
            
            except Exception as Exec:
                not_send.append(person[0])
                logger.error('Произошла ошибка:\n{}'.format(Exec),
                             user_id=call.message.chat.id)
                continue
            
            # bot.send_document(chat_id=person,
            #                   document=open(admin_manual_dir + admin_manual_name, 'rb'))
        
        t = await bot.send_message(
            chat_id=call.message.chat.id,
            text='Бот разослал сообщения пользователям из базы данных.\n'
                 'Текст сообщения:\n'
                 '{new_msg}\n'
                 '\n'
                 'Всего сообщений: {qty_m} штук\n'
                 '\n'
                 'Не найдены пользователи: {not_found}\n'
                 '\n'
                 'Не отправлено пользователям из-за ошибок: {not_send}'.format(
                new_msg=update_msg_text,
                qty_m=count_txt - len(not_found) - len(not_send),
                not_found=not_found,
                not_send=not_send))
        
        logger.info(t.text,
                    user_id=call.message.chat.id)
