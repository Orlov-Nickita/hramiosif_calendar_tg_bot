"""
Модуль обработки админ команды на работу с лог-файлом
"""

import os
import emoji
from keyboards_for_bot.admin_keyboards import IKM_admin_log_remove_conf, IKM_admin_errors_log_send
from loader import bot, administrators, log_file_name, log_dir, temp_error_file, dp
from utils.custom_funcs import button_text
from utils.logger import logger
from aiogram.types import Message, CallbackQuery, ParseMode, ChatActions


async def upload_logs(message: Message) -> None:
    """
    Функция для получения файла с логами.
    :param message: Сообщение от пользователя.
    :return: Файл с логами.
    """
    logger.info("Запущена функция admin_logs.upload_logs", username=message.chat.username, user_id=message.chat.id)

    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.UPLOAD_DOCUMENT)

    await bot.send_document(chat_id=message.chat.id, document=open(log_dir + log_file_name, "rb"))

    logger.info("Бот отправил файл с логами", user_id=message.chat.id)


err_count = 0
err_text = ""


async def check_errors(message: Message) -> None:
    """
    Функция для анализа ошибок.
    :param message: Сообщение от пользователя.
    :return: Количество ошибок.
    """
    logger.info("Запущена функция admin_logs.check_errors", username=message.chat.username, user_id=message.chat.id)

    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.TYPING)

    global err_count
    global err_text
    err_count = 0
    err_text = ""

    with open(log_dir + log_file_name, "r", encoding="utf-8") as file:

        for line in file.readlines():
            error = " ".join(line.split("\n"))

            if "[error]" in error.lower() or "[warning]" in error.lower():
                err_count += 1
                err_text += f"{err_count}: {error}\n\n"

            if err_text:
                async with open(log_dir + temp_error_file, "w", encoding="utf-8") as tempfile:
                    await tempfile.write(err_text)

    if err_count == 0:
        msg = await bot.send_message(
            chat_id=message.chat.id,
            text=" {emoji1} Ошибок не найдено".format(emoji1=emoji.emojize(":white_check_mark:", language="alias")),
        )

    else:
        msg = await bot.send_message(
            chat_id=message.chat.id,
            text=" {emoji1} Найдено ошибок {qty}".format(
                qty=err_count, emoji1=emoji.emojize(":red_circle:", language="alias")
            ),
            reply_markup=IKM_admin_errors_log_send(),
        )

    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text), user_id=message.chat.id)


async def remove_logs(message: Message) -> None:
    """
    Функция очистки файла с логами.
    :param message: Сообщение от пользователя.
    :return: Очистка файла.
    """
    logger.info("Запущена функция admin_logs.remove_logs", username=message.chat.username, user_id=message.chat.id)

    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.FIND_LOCATION)

    if message.chat.id == int(administrators["Никита"]):

        msg = await bot.send_message(
            chat_id=message.chat.id, text="Подтвердите удаление", reply_markup=IKM_admin_log_remove_conf()
        )

    else:
        msg = await bot.send_message(chat_id=message.chat.id, text="У Вас нет прав доступа")

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Пользователь пытался удалить лог-файл:\n"
            "tg_id: <code>{id}</code>\n"
            "username: <code>{user}</code>\n"
            "name: <code>{name}</code>\n"
            "surname: <code>{surname}</code>\n".format(
                id=message.chat.id,
                user=message.from_user.username,
                name=message.from_user.first_name,
                surname=message.from_user.last_name,
            ),
            parse_mode=ParseMode.HTML,
        )

    logger.info('Бот отправил сообщение\n"{}"'.format(msg.text), user_id=message.chat.id)


@dp.callback_query_handler(lambda call: call.data == "yes_remove_log" or call.data == "no_remove_log")
async def remove_log_confirm(call: CallbackQuery) -> None:
    """
    Обработка нажатия на клавиатуре с подтверждением удаления лог файла
    param call: Нажатая кнопка на клавиатуре
    return: Либо происходит очистка файла, либо отмена и при условии, что это выбрал определенный пользователь
    """
    logger.info(
        'Запущена функция remove_log_confirm, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    if call.data == "no_remove_log":

        await bot.send_message(chat_id=call.message.chat.id, text="Удаление отменено")

        logger.info("Удаление отменено", user_id=call.message.chat.id)

    else:

        try:
            async with open(log_dir + log_file_name, "r+") as log_file:
                await log_file.truncate()

        except PermissionError as PerErr:
            await bot.send_message(chat_id=call.message.chat.id, text="Лог-файл очистить не получилось")

            logger.error(f"Ошибка {PerErr}", user_id=call.message.chat.id)

        else:
            await bot.edit_message_text(
                chat_id=call.message.chat.id, message_id=call.message.message_id, text="Лог-файл очищен"
            )


@dp.callback_query_handler(lambda call: call.data == "yes_send_errors_log" or call.data == "no_remove_log")
async def send_errors_log(call: CallbackQuery) -> None:
    """
    Обработка нажатия на клавиатуре с подтверждением удаления лог файла
    param call: Нажатая кнопка на клавиатуре
    return: Либо происходит очистка файла, либо отмена и при условии, что это выбрал определенный пользователь
    """
    logger.info(
        'Запущена функция send_errors_log, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    if call.data == "yes_send_errors_log":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)

        await bot.send_document(chat_id=call.message.chat.id, document=open(log_dir + temp_error_file, "rb"))
        os.remove(log_dir + temp_error_file)
