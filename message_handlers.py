"""
Модуль со всеми командами, которые может обрабатывать бот
"""

from commands import c_start, c_help, c_keyboard, admin_panel, t_schedule, t_send_qr_code
from loader import bot, administrators, dp
from utils.logger import logger
from aiogram.types import ParseMode, Message


@dp.message_handler(commands=["start"])
async def send_welcome_func(message: Message) -> None:
    """
    Отправляет Пользователю стартовое сообщение
    :param message: В качестве параметра передается сообщение из чата
    :type message: aiogram.types.Message
    :return: Отправляется сообщение в чат
    :rtype aiogram.types.Message
    """
    logger.info("Запущена команда /start", username=message.from_user.username, user_id=message.chat.id)
    await c_start.start(message)


@dp.message_handler(commands=["help"])
async def help_command_func(message: Message) -> None:
    """
    Отправляет Пользователю вспомогательное сообщение с подсказками
    :param message: В качестве параметра передается сообщение из чата
    :type message: aiogram.types.Message
    :return: Отправляется сообщение в чат
    :rtype aiogram.types.Message
    """
    logger.info("Запущена команда /help", username=message.from_user.username, user_id=message.chat.id)

    await c_help.start(message)


@dp.message_handler(commands=["keyboard"])
async def keyboard_open(message: Message) -> None:
    """
    Открывает Пользователю клавиатуру внизу
    :param message: В качестве параметра передается сообщение из чата
    :type message: aiogram.types.Message
    :return: Отправляется сообщение в чат
    :rtype aiogram.types.Message
    """
    logger.info("Запущена команда /keyboard", username=message.from_user.username, user_id=message.chat.id)

    await c_keyboard.start(message)


@dp.message_handler(commands=["admin", "Admin"])
async def admin_panel_func(message: Message) -> None:
    """
    Открывает панель управления для администраторов
    :param message: В качестве параметра передается сообщение из чата
    :type message: aiogram.types.Message
    :return: Отправляется сообщение в чат
    :rtype aiogram.types.Message
    """
    logger.info("Запущена команда /admin", username=message.from_user.username, user_id=message.chat.id)

    if str(message.chat.id) in administrators.values():
        await admin_panel.start(message)

    else:
        await bot.send_message(chat_id=message.chat.id, text="У Вас нет прав доступа")

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Пользователь "
            "пытался получить доступ к администрированию:\n"
            "tg_id: <code>{id}</code>\n"
            "Ник: <code>{user}</code>\n"
            "Имя: <code>{name}</code>\n"
            "Фамилия: <code>{surname}</code>\n".format(
                id=message.chat.id,
                user=message.from_user.username,
                name=message.from_user.first_name,
                surname=message.from_user.last_name,
            ),
            parse_mode=ParseMode.HTML,
        )


@dp.message_handler(content_types=["text"])
async def text_func(message: Message) -> None:
    """
    Функция, которая реагирует на сообщение пользователя из чата.
    :param message: В качестве параметра передается сообщение из чата
    :type message: aiogram.types.Message
    :return: None
    :rtype: aiogram.types.Message

    """
    logger.info("Запущена команда /text", username=message.from_user.username, user_id=message.chat.id)

    if message.text.startswith("Уточнить расписание богослужений"):
        await t_schedule.start(message)

    elif message.text.startswith("Пожертвовать храму"):
        await t_send_qr_code.send_qrcode(message)

    # elif message.text.startswith('Задать вопрос священнику'):
    #     await t_question.start(message)
    #
    # elif message.text.startswith('Посмотреть календарь'):
    # await send_information.start(message)

    else:
        logger.info(
            'Пользователь написал "{}"'.format(message.text),
            username=message.from_user.username,
            user_id=message.chat.id,
        )

        msg = await bot.send_message(chat_id=message.chat.id, text="Выберите пункт меню\n")

        logger.info('Бот ответил "{}"'.format(msg.text), user_id=message.chat.id)
