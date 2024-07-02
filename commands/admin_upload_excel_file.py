"""
Модуль обработки админ команды на загрузку Excel файла
"""

import emoji
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import os.path
from keyboards_for_bot.admin_keyboards import IKM_admin_overwrite_excel_file
from loader import bot, schedules_excel_dir, excel_file_name, dp, administrators
from utils.custom_funcs import load_photo_or_doc_from_bot, button_text
from utils.logger import logger


class ExcelFileDownload(StatesGroup):
    """
    Машина состояний
    get_file: Для процесса первичной загрузки файла
    change_file: Для процесса перезаписи
    file_id: Id файла
    src: Путь записи файла
    downloaded_file: Байт-строка скачанного файла
    """

    get_file = State()
    change_file = State()
    file_id = ""
    src = ""
    downloaded_file = b""


async def start(message: Message) -> None:
    """
    Стартовая функция загрузки документа Excel с расписанием
    :param message: Сообщение от пользователя.
    :return: Отправляется сообщение и ожидается файл от пользователя
    """
    logger.info(
        "Запущена функция admin_upload_excel_file.start", username=message.chat.username, user_id=message.chat.id
    )

    await ExcelFileDownload.get_file.set()

    msg = await bot.send_message(chat_id=message.chat.id, text='Пришли файл в формате ".xlsx"')

    logger.info('Бот отправил сообщение "{}"'.format(msg.text), user_id=message.chat.id)


@dp.message_handler(lambda message: message.text == "Отмена" or message.text == "отмена", state=ExcelFileDownload)
async def cancel_upload(message: Message, state: FSMContext) -> None:
    """
    Функция обработчик отмены действий
    :param message: Сообщение от пользователя.
    :param state: Состояние машины состояний
    """
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(text="Загрузка отменена", chat_id=message.chat.id)
    await state.finish()


@dp.message_handler(content_types=["document"], state=ExcelFileDownload.get_file)
async def upload_excel_file_func(message: Message, state: FSMContext) -> None:
    """
    Функция обработки полученного файла. Если такой есть, то предлагает перезаписать
    param message: Файл с Excel таблицей.
    """
    logger.info(
        "Запущена функция upload_excel_file_func пользователь отправил в бот файл",
        username=message.chat.username,
        user_id=message.chat.id,
    )

    async with state.proxy() as data:
        t = data["get_file"] = await bot.get_file(message.document.file_id)

    if not os.path.exists(schedules_excel_dir):
        os.makedirs(schedules_excel_dir)

    if message.document is None:
        logger.error(
            "Пользователь отправил {}".format(message), username=message.chat.username, user_id=message.chat.id
        )

        msg = await bot.send_message(
            chat_id=message.chat.id, text='Ошибка. Нужен файл. Повторите отправку или отправьте команду "Отмена"'
        )

        logger.info('Бот отправил сообщение "{}"'.format(msg.text), user_id=message.chat.id)

    elif os.path.splitext(t.file_path)[1] != ".xlsx":
        logger.error(
            "Пользователь отправил файл с неправильным форматом {}".format(os.path.splitext(t.file_path)[1]),
            username=message.chat.username,
            user_id=message.chat.id,
        )

        msg = await bot.send_message(
            chat_id=message.chat.id,
            text='Ошибка. Нужен файл в формате ".xlsx". Повторите отправку или отправьте ' 'команду "Отмена"',
        )

        logger.info('Бот отправил сообщение "{}"'.format(msg.text), user_id=message.chat.id)

    else:
        async with state.proxy() as data:
            temp = await bot.download_file(data["get_file"].file_path)
            data["downloaded_file"] = downloaded_file = temp.getbuffer().tobytes()
            data["src"] = src = schedules_excel_dir + excel_file_name

        if os.path.exists(src):
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text="Excel уже есть. Перезаписать?",
                reply_markup=IKM_admin_overwrite_excel_file(),
            )

            await ExcelFileDownload.change_file.set()

            logger.info('Бот отправил сообщение "{}"'.format(msg.text), user_id=message.chat.id)

        else:
            try:
                await load_photo_or_doc_from_bot(
                    bot=bot,
                    logger=logger,
                    msg=message,
                    src=src,
                    downloaded_file=downloaded_file,
                    bot_text="Excel сохранен",
                    doc=True,
                    state=state,
                )
            except:
                await bot.send_message(chat_id=message.chat.id, text="Файл нечитаемый. Операция отменена")
                await state.finish()
                await bot.send_message(
                    chat_id=administrators["Никита"],
                    text="Пользователь {id} пытался добавить Excel файл. Файл битый".format(id=message.chat.id),
                )

            else:
                await bot.send_message(
                    chat_id=administrators["Никита"],
                    text="Пользователь {id} добавил Excel файл".format(id=message.chat.id),
                )
                await state.finish()


@dp.callback_query_handler(
    lambda call: (call.data == "yes_overwrite_excel" or call.data == "no_leave_excel")
    and "Excel уже есть. Перезаписать?" in call.message.text,
    state=ExcelFileDownload.change_file,
)
async def overwrite_excel_func(call: CallbackQuery, state: FSMContext) -> None:
    """
    Функция для перезаписи файла Excel
    param call: Нажатая клавиша клавиатуры.
    """
    async with state.proxy() as data:
        downloaded_file = data["downloaded_file"]
        src = data["src"]

    logger.info(
        'Запущена функция overwrite_excel_func, пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    if call.data == "yes_overwrite_excel":
        temp_mg = await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Минутку...{emoji}".format(emoji=emoji.emojize(":hourglass:", language="alias")),
        )

        try:
            await load_photo_or_doc_from_bot(
                bot=bot,
                logger=logger,
                msg=call.message,
                src=src,
                downloaded_file=downloaded_file,
                bot_text="Файл перезаписан, Excel сохранен",
                doc=True,
                state=state,
            )
        except:
            await bot.send_message(chat_id=call.message.chat.id, text="Файл нечитаемый. Операция отменена")
            await state.finish()
            await bot.send_message(
                chat_id=administrators["Никита"],
                text="Пользователь {id} пытался добавить Excel файл. Файл битый".format(id=call.message.chat.id),
            )

        else:
            await bot.send_message(
                chat_id=administrators["Никита"],
                text="Пользователь {id} перезаписал Excel файл".format(id=call.message.chat.id),
            )
            await state.finish()
            await bot.delete_message(chat_id=call.message.chat.id, message_id=temp_mg.message_id)

    if call.data == "no_leave_excel":
        msg = await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Файл не перезаписан, операция отменена",
        )
        await state.finish()

        logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text), user_id=call.message.chat.id)
