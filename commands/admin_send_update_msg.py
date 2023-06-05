"""
Модуль обработки админ команды на отправку сообщения с обновлениями
"""

import time
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ParseMode, CallbackQuery
from keyboards_for_bot.admin_keyboards import IKM_admin_update_send_conf
from loader import bot, administrators, dp
from loader import users_sql_dir, users_sql_file_name
from utils.custom_funcs import button_text
from utils.logger import logger
from utils.sql_funcs import get_info_from_sql_for_followers


class UpdateMsgSend(StatesGroup):
    """
    Машина состояний
    TODO
    """
    get_msg = State()
    send_msg = State()
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
    
    if message.chat.id == int(administrators['Никита']):
        await UpdateMsgSend.get_msg.set()
        
        await bot.send_message(chat_id=message.chat.id,
                               text='Что отправим?')


@dp.message_handler(content_types=['text'], state=UpdateMsgSend.get_msg)
async def preparation_before_send(message: Message, state: FSMContext) -> None:
    """
    TODO
    """
    logger.info(
        'Запущена функция preparation_before_send',
        username=message.from_user.username,
        user_id=message.chat.id)
    
    async with state.proxy() as data:
        upd_txt = data['get_msg'] = message.text
    
    await bot.send_message(chat_id=message.chat.id,
                           text=upd_txt,
                           reply_markup=IKM_admin_update_send_conf())
    
    await UpdateMsgSend.send_msg.set()


@dp.callback_query_handler(
    lambda call: call.data == 'yes_send_upd_msg' or call.data == 'no_send_upd_msg', state=UpdateMsgSend.send_msg)
async def send_update_msg_confirm(call: CallbackQuery, state: FSMContext) -> None:
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
        await state.finish()
        
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
        
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Отправка сообщения отменена')
        
        logger.info('Отправка сообщения отменена',
                    user_id=call.message.chat.id)
    
    else:
        async with state.proxy() as data:
            upd_txt = data['get_msg'] = call.message.text
        
        # all_persons = await get_info_from_sql_for_followers(sql_base=users_sql_dir + users_sql_file_name,
        #                                                     message=call.message)
        
        # all_persons = [459901923, 434895679, 949421028]
        # all_persons = [949421028, 5022408096, 12444114124412421412]
        # all_persons = [(5022408096,), (1201283009,), (1765957161,), (345707936,), (1692880786,)]
        all_persons = [(949421028,), (5022408096,)]

        count_txt = 0
        not_found = []
        not_send = []
        for person in all_persons:
            time.sleep(0.5)
            
            try:
                await bot.send_message(chat_id=person[0],
                                       text=upd_txt,
                                       parse_mode=ParseMode.HTML)
                count_txt += 1
                
                logger.info('Сообщение № {}.\n'
                            'Отправлено пользователю {}'.format(count_txt, person[0]),
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
                new_msg=upd_txt,
                qty_m=count_txt,
                not_found=not_found,
                not_send=not_send))
        
        logger.info(t.text,
                    user_id=call.message.chat.id)
        
        await state.finish()
