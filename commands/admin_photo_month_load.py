"""
Модуль обработки админ команды на загрузку месячного расписания
"""

import pytz
import os.path
import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from errors import FileError
from keyboards_for_bot.admin_keyboards import (
    IKM_admin_save_photo_again,
    IKM_admin_month_save_photo,
    IKM_admin_overwrite_file_first_choice,
    IKM_admin_overwrite_file_second_choice,
)
from loader import bot, schedule_photo_month_dir, month_photo_name, all_months_in_calendar_for_save, dp, administrators
from utils.logger import logger
from utils.custom_funcs import button_text, load_photo_or_doc_from_bot
from aiogram.types import Message, CallbackQuery, ParseMode


class MonthPhotoDownload(StatesGroup):
    """
    Машина состояний
    get_file: Для процесса первичной загрузки файла
    month_choice: Для процесса выбора месяца (текущий, следующий, другой)
    first_change_file: Для процесса первичной перезаписи
    second_change_file: Для процесса вторичной перезаписи (когда уточняется точно ли перезаписать)
    month_number_choice: Для выбора числа месяца
    file_id: Id файла
    src: Путь записи файла
    downloaded_file: Байт-строка скачанного файла
    """

    get_file = State()
    month_choice = State()
    first_change_file = State()
    second_change_file = State()
    month_number_choice = State()
    file_id = ""
    src = ""
    downloaded_file = b""


async def start_month(message: Message) -> None:
    """
    Стартовая функция начала процесса загрузки фотографий.
    :param message: Сообщение от пользователя.
    :return: Сообщение от бота и ожидание фотографии.
    """
    logger.info(
        "Запущена функция admin_photo_month_load.start_month", username=message.chat.username, user_id=message.chat.id
    )

    await MonthPhotoDownload.get_file.set()

    msg = await bot.send_message(chat_id=message.chat.id, text="Пришли расписание на месяц и я сохраню")

    logger.info('Бот отправил сообщение "{}"'.format(msg.text), user_id=message.chat.id)


@dp.message_handler(lambda message: message.text == "Отмена" or message.text == "отмена", state=MonthPhotoDownload)
async def cancel_upload(message: Message, state: FSMContext) -> None:
    """
    Функция обработчик отмены действий
    :param message: Сообщение от пользователя.
    :param state: Состояние машины состояний
    """
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(text="Загрузка отменена", chat_id=message.chat.id)
    await state.finish()


@dp.message_handler(content_types=["text", "document", "photo"], state=MonthPhotoDownload.get_file)
async def photo_month(message: Message, state: FSMContext) -> None:
    """
    Функция обработчик присланного файла
    :param message: Сообщение от пользователя.
    :param state: Состояние машины состояний
    """
    logger.info(
        "Запущена функция photo_month пользователь отправил в бот файл",
        username=message.chat.username,
        user_id=message.chat.id,
    )

    try:
        if not os.path.exists(schedule_photo_month_dir):
            os.makedirs(schedule_photo_month_dir)

        elif message.document and "pdf" in message.document.mime_type:

            logger.info(
                "Пользователь прислал файл. Тип файла {}".format(message.document.mime_type),
                username=message.chat.username,
                user_id=message.chat.id,
            )

            async with state.proxy() as data:
                data["get_file"] = await bot.get_file(message.document.file_id)

            await MonthPhotoDownload.month_choice.set()

        else:
            raise FileError

    except FileError:
        logger.error(
            "Ошибка формата файла FileError {}".format(message),
            username=message.from_user.username,
            user_id=message.chat.id,
        )
        await bot.send_message(
            chat_id=message.chat.id, text='Ошибка. Нужен файл PDF. Повторите отправку или отправьте команду "Отмена"'
        )
    else:
        msg = await bot.send_message(
            text="На какой месяц это расписание?", chat_id=message.chat.id, reply_markup=IKM_admin_month_save_photo()
        )

        logger.info('Бот отправил сообщение "{}"'.format(msg.text), user_id=message.chat.id)


@dp.callback_query_handler(
    lambda call: call.data in ["this_month", "next_month", "other_month"]
    and "На какой месяц это расписание" in call.message.text,
    state=MonthPhotoDownload.month_choice,
)
async def save_photo_month(call: CallbackQuery, state: FSMContext) -> None:
    """
    Функция обработчик первой клавиатуры с определением номера месяца
    """
    logger.info(
        'Запущена функция save_photo_month, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    async with state.proxy() as data:
        temp = await bot.download_file(data["get_file"].file_path)
        data["downloaded_file"] = downloaded_file = temp.getbuffer().tobytes()

    if call.data == "this_month" or call.data == "next_month":
        if call.data == "this_month":
            month_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%m"))
            make_excel_file: bool = True

        else:
            month_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%m")) + 1
            make_excel_file: bool = False

        current_month = all_months_in_calendar_for_save[month_digit - 1]
        year_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%Y"))

        try:
            async with state.proxy() as data:
                data["src"] = src = schedule_photo_month_dir + month_photo_name.format(
                    month=current_month, year=year_digit
                )

        except AttributeError as AEerror:
            logger.error(
                "Произошла ошибка {}".format(AEerror),
                username=call.message.from_user.username,
                user_id=call.message.chat.id,
            )
            await bot.send_message(
                chat_id=call.message.chat.id,
                text="Неверный формат файла, нужен файл PDF. Повторите отправку или отправьте " 'команду "Отмена"',
            )

            await MonthPhotoDownload.get_file.set()

        else:
            if os.path.exists(src):
                msg = await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Файл с расписанием на указанный месяц уже есть. Перезаписать?",
                    reply_markup=IKM_admin_overwrite_file_first_choice(),
                )

                logger.info(
                    'Бот отредактировал сообщение и написал "{}"'.format(msg.text), user_id=call.message.chat.id
                )

                await MonthPhotoDownload.first_change_file.set()

            else:
                await load_photo_or_doc_from_bot(
                    bot=bot,
                    logger=logger,
                    msg=call.message,
                    src=src,
                    doc=True,
                    downloaded_file=downloaded_file,
                    make_excel_file=make_excel_file,
                    bot_text="Расписание на месяц загружено",
                    keyboard=IKM_admin_save_photo_again(),
                    state=state,
                )

                await bot.send_message(
                    chat_id=administrators["Никита"],
                    text="Пользователь {id} добавил расписание на месяц".format(id=call.message.chat.id),
                )
                await state.finish()

    elif call.data == "other_month":
        await MonthPhotoDownload.month_number_choice.set()

        msg = await bot.send_message(
            chat_id=call.message.chat.id,
            text="Укажите номер месяца в году. Сейчас, например, идет {} месяц".format(
                int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%m"))
            ),
        )

        logger.info('Бот отправил сообщение "{}"'.format(msg.text), user_id=call.message.chat.id)


@dp.message_handler(state=MonthPhotoDownload.month_number_choice)
async def download_photo_month(message: Message, state: FSMContext) -> None:
    """
    Функция загрузки фотографии. Бот проверяет наличие и сохраняет или предлагает перезаписать
    """
    logger.info("Запущена функция download_photo_month", username=message.from_user.username, user_id=message.chat.id)

    if message.text.isdigit():

        current_month = all_months_in_calendar_for_save[int(message.text) - 1]
        year_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%Y"))

        try:
            async with state.proxy() as data:
                downloaded_file = data["downloaded_file"]
                data["src"] = src = schedule_photo_month_dir + month_photo_name.format(
                    month=current_month, year=year_digit
                )

        except AttributeError as AEerror:
            logger.error(
                "Произошла ошибка {}".format(AEerror), username=message.from_user.username, user_id=message.chat.id
            )
            await bot.send_message(
                chat_id=message.chat.id,
                text="Неверный формат файла, нужен файл PDF. Повторите отправку или отправьте " 'команду "Отмена"',
            )

            await MonthPhotoDownload.get_file.set()
        else:
            if os.path.exists(src):
                msg = await bot.send_message(
                    chat_id=message.chat.id,
                    text="Файл с расписанием на указанный месяц уже есть. Перезаписать?",
                    reply_markup=IKM_admin_overwrite_file_first_choice(),
                )

                logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text), user_id=message.chat.id)

                await MonthPhotoDownload.first_change_file.set()

            else:
                await load_photo_or_doc_from_bot(
                    bot=bot,
                    logger=logger,
                    msg=message,
                    src=src,
                    downloaded_file=downloaded_file,
                    bot_text="Расписание на месяц загружено",
                    other_week=True,
                    keyboard=IKM_admin_save_photo_again(),
                    state=state,
                )

                await bot.send_message(
                    chat_id=administrators["Никита"],
                    text="Пользователь {id} добавил расписание на месяц".format(id=message.chat.id),
                )
                await state.finish()
    else:
        msg = await bot.send_message(
            chat_id=message.chat.id, text='Ошибка. Нужно просто одно число или отправьте команду "Отмена"'
        )
        logger.info('Бот написал "{}"'.format(msg.text), user_id=message.chat.id)


@dp.callback_query_handler(
    lambda call: (call.data == "yes_overwrite" or call.data == "no_overwrite")
    and "Файл с расписанием на указанный месяц уже есть. Перезаписать?" in call.message.text,
    state=MonthPhotoDownload.first_change_file,
)
async def overwrite_month(call: CallbackQuery, state: FSMContext) -> None:
    """
    Функция обработчик для перезаписи файла или проверки имеющегося в записи
    """
    logger.info(
        'Запущена функция overwrite_month, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    async with state.proxy() as data:
        downloaded_file = data["downloaded_file"]
        src = data["src"]

    if call.data == "yes_overwrite":
        month_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%m"))
        current_month = all_months_in_calendar_for_save[month_digit - 1].lower()

        if current_month in src.lower():
            make_excel_file = True
        else:
            make_excel_file = False

        await load_photo_or_doc_from_bot(
            bot=bot,
            logger=logger,
            msg=call.message,
            src=src,
            doc=True,
            make_excel_file=make_excel_file,
            downloaded_file=downloaded_file,
            bot_text="Файл перезаписан, расписание на месяц загружено",
            keyboard=IKM_admin_save_photo_again(),
            state=state,
        )

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Пользователь {id} добавил расписание на месяц".format(id=call.message.chat.id),
        )
        await state.finish()

    elif call.data == "no_overwrite":

        msg = await bot.edit_message_text(
            text="Файл с расписанием на указанный месяц уже есть. Перезаписать?\n"
            "<i>- <code>Вы выбрали {button}</code></i>".format(button=button_text(call)),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode=ParseMode.HTML,
        )

        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text), user_id=call.message.chat.id)

        msg = await bot.send_document(
            chat_id=call.message.chat.id,
            document=open(src, "rb"),
            reply_markup=IKM_admin_overwrite_file_second_choice(),
        )
        await MonthPhotoDownload.second_change_file.set()

        logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text), user_id=call.message.chat.id)


@dp.callback_query_handler(
    lambda call: (call.data == "yes_overwrite_final" or call.data == "no_overwrite_final"),
    state=MonthPhotoDownload.second_change_file,
)
async def overwrite_month_2(call: CallbackQuery, state: FSMContext) -> None:
    """
    Функция обработчик окончательного принятия решения по перезаписи файла или отмене от операции
    """
    logger.info(
        'Запущена функция overwrite_month_2, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    if call.data == "yes_overwrite_final":
        async with state.proxy() as data:
            downloaded_file = data["downloaded_file"]
            src = data["src"]

        await load_photo_or_doc_from_bot(
            bot=bot,
            logger=logger,
            msg=call.message,
            src=src,
            downloaded_file=downloaded_file,
            bot_text="Файл перезаписан, расписание на месяц загружено",
            keyboard=IKM_admin_save_photo_again(),
            photo=True,
            state=state,
        )

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Пользователь {id} добавил расписание на месяц".format(id=call.message.chat.id),
        )

        await state.finish()

    elif call.data == "no_overwrite_final":
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        await bot.send_message(chat_id=call.message.chat.id, text="Файл не перезаписан, операция отменена")
        await state.finish()
