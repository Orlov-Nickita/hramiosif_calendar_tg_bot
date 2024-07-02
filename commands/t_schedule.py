"""
Модуль для обработки команды на отправку расписания
"""

import datetime
import os.path
import emoji
import pytz
from excel_utils.open_check_funcs import data_from_json
from excel_utils.parsing_funcs import schedule_for_a_specific_day, schedule_for_some_days
from loader import (
    bot,
    all_months_in_calendar,
    schedules_excel_dir,
    json_days_list,
    schedule_photo_week_dir,
    week_photo_name,
    month_photo_name,
    schedule_photo_month_dir,
    all_months_in_calendar_for_save,
    administrators,
    dp,
)
from utils.logger import logger
from keyboards_for_bot.keyboards import (
    IKM_schedule_option,
    IKM_date_schedule_choice,
    IKM_open_schedule,
    IKM_week_schedule_choice_1,
    IKM_week_schedule_choice_2,
)
from utils.custom_funcs import button_text
from aiogram.types import Message, CallbackQuery, ChatActions, ParseMode

############################################
"""
Старт
"""


async def start(message: Message) -> None:
    """
    Стартовая функция формирования ответа на запрос расписания
    :param message: Сообщение от пользователя из чата
    :return: Бот обрабатывает сообщение и направляет ответ
    """

    logger.info(
        'Запущена функция t_schedule.start пользователь написал "{}"'.format(message.text),
        username=message.from_user.username,
        user_id=message.chat.id,
    )
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.TYPING)

    if message.text.startswith("Уточнить расписание богослужений"):
        """
        В данном случае посылается на обработку запрос в функцию IKM_date_schedule_choice для вывода кнопок с датами
        """
        msg = await bot.send_message(
            chat_id=message.chat.id,
            text="Вы хотите уточнить расписание богослужений",
            reply_markup=IKM_schedule_option(),
        )

        logger.info('Бот ответил "{}"'.format(msg.text), user_id=message.chat.id)

    else:
        """
        В данном случае была введена команда, которую бот еще не понимает и потому бот отправляет сообщение с просьбой
        выбрать пункт меню
        """
        msg = await bot.send_message(chat_id=message.chat.id, text="Выберите пункт меню")

        logger.info('Бот ответил "{}"'.format(msg.text), user_id=message.chat.id)


############################################
"""
Выбор из меню расписания на один день
"""


@dp.callback_query_handler(
    lambda call: call.message.content_type == "text"
    and call.message.text.startswith("Вы хотите уточнить расписание богослужений")
    and call.data == "day"
)
async def day_choice_keyboard_callback(call: CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Выбран пункт "День"
    """
    logger.info(
        'Запущена функция day_choice_keyboard_callback пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.TYPING)

    try:
        days = [i for i in data_from_json(schedules_excel_dir + json_days_list) if i != "-"]
        msg = await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="На какой день Вы хотели посмотреть расписание?",
            reply_markup=IKM_date_schedule_choice(days_list=days),
        )

    except (FileNotFoundError, ValueError) as Exec:
        logger.error("Произошла ошибка:\n{}".format(Exec), user_id=call.message.chat.id)

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Произошла ошибка в функции day_choice_keyboard_callback "
            "у пользователя {id}. Попросили расписание на день\n"
            "{exec}".format(id=call.message.chat.id, exec=Exec),
        )

        msg = await bot.send_message(
            chat_id=call.message.chat.id,
            text="К сожалению, расписания пока нет. Ожидаем "
            "информацию от Храма. Сделаем уведомление, когда расписание будет "
            "загружено. Спасибо, что пользуетесь нашим Ботом {}".format(
                emoji.emojize(":upside_down_face:", language="alias")
            ),
        )

    except Exception as Exec:
        logger.error("Произошла ошибка:\n{}".format(Exec), user_id=call.message.chat.id)

        await bot.send_message(
            chat_id=administrators["Никита"],
            text="Произошла ошибка в функции day_choice_keyboard_callback "
            "у пользователя {id}\n"
            "\n"
            "{exec}".format(id=call.message.chat.id, exec=Exec),
        )

        msg = await bot.send_message(
            chat_id=call.message.chat.id,
            text="Приносим извинения, возникла непредвиденная ошибка. Технические специалисты "
            "уже работают над решением проблемы",
        )

    logger.info('Бот ответил "{}"'.format(msg.text), user_id=call.message.chat.id)


############################################
"""
Отправка расписания на конкретный день
"""


@dp.callback_query_handler(
    lambda call: call.message.content_type == "text"
    and call.message.text.startswith("На какой день Вы хотели посмотреть расписание")
    and call.data != "open_again"
)
async def date_choice_keyboard_callback(call: CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Это для меню на конкретный день
    """
    logger.info(
        'Запущена функция date_choice_keyboard_callback пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.TYPING)

    if call.data == "return":

        logger.info(
            'Пользователь нажал на кнопку "{}"'.format(button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id,
        )

        await bot.edit_message_text(
            text="Вы хотите уточнить расписание богослужений",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_schedule_option(),
        )

    else:

        logger.info(
            'Пользователь нажал на кнопку "{}"'.format(button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id,
        )

        msg = await bot.edit_message_text(
            text="На какой день Вы хотели посмотреть расписание?\n"
            "<i>- <code>Вы выбрали {button}</code></i>".format(button=button_text(call)),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_open_schedule(),
            parse_mode=ParseMode.HTML,
        )

        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text), user_id=call.message.chat.id)

        await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.TYPING)

        try:
            schedule = schedule_for_a_specific_day(
                day=call.data, username=call.message.from_user.username, user_id=call.message.chat.id
            )

            msg = await bot.send_message(chat_id=call.message.chat.id, text=schedule, parse_mode=ParseMode.HTML)

            logger.info(
                'Пользователь нажал на кнопку "{}"'.format(button_text(call)),
                username=call.message.from_user.username,
                user_id=call.message.chat.id,
            )

            logger.info(
                "Пользователь выбрал дату {date}".format(date=call.data),
                username=call.message.from_user.username,
                user_id=call.message.chat.id,
            )

            logger.info('Бот ответил "{}"'.format(msg.text), user_id=call.message.chat.id)

        except Exception as Exec:
            logger.error("Произошла ошибка:\n{}".format(Exec), user_id=call.message.chat.id)

            await bot.send_message(
                chat_id=administrators["Никита"],
                text="Произошла ошибка в функции date_choice_keyboard_callback "
                "у пользователя {id}\n"
                "\n"
                "{exec}".format(id=call.message.chat.id, exec=Exec),
            )

            await bot.send_message(
                chat_id=call.message.chat.id,
                text="Приносим извинения, возникла непредвиденная ошибка. Технические специалисты "
                "уже работают над решением проблемы",
            )


############################################
"""
Выбор из меню расписания на неделю
"""


@dp.callback_query_handler(
    lambda call: call.message.content_type == "text"
    and call.message.text.startswith("Вы хотите уточнить расписание богослужений")
    and (call.data == "week" or call.data == "next_week")
)
async def week_choice_keyboard_callback(call: CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Выбран пункт "Неделя". Предлагается выбор между текстом и файлом
    """

    logger.info(
        'Запущена функция week_choice_keyboard_callback пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    if call.data == "week":
        msg = await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Вы хотели посмотреть расписание на текущую неделю. " "Выберите удобный вариант",
            reply_markup=IKM_week_schedule_choice_1(),
        )

    else:
        msg = await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Вы хотели посмотреть расписание на следующую неделю. " "Выберите удобный вариант",
            reply_markup=IKM_week_schedule_choice_2(),
        )

    logger.info('Бот ответил "{}"'.format(msg.text), user_id=call.message.chat.id)


############################################
"""
Отправка расписания на текущую неделю
"""


@dp.callback_query_handler(
    lambda call: call.message.content_type == "text"
    and call.message.text.startswith("Вы хотели посмотреть расписание на текущую неделю")
    and call.data != "open_again"
)
async def date_choice_keyboard_callback_this_week(call: CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Это для меню на неделю
    """
    logger.info(
        "Запущена функция date_choice_keyboard_callback_this_week, "
        'пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    if call.data == "text_schedule_this":
        await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.TYPING)

        try:
            today_digit = datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%d")
            month_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%m"))

            current_date = "{day} {month}".format(day=today_digit, month=all_months_in_calendar[month_digit - 1])

            days_till_week_end = 8 - datetime.datetime.now(pytz.timezone("Europe/Moscow")).isoweekday()

            all_days_in_schedule = [i for i in data_from_json(schedules_excel_dir + json_days_list) if i != "-"]

            current_day = all_days_in_schedule.index(current_date)

            rest_week = all_days_in_schedule[current_day : current_day + days_till_week_end]

            await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.TYPING)

            week_schedule = schedule_for_some_days(
                days=rest_week,
                username=call.message.from_user.username,
                user_id=call.message.chat.id,
            )

            msg = await bot.send_message(chat_id=call.message.chat.id, text=week_schedule, parse_mode=ParseMode.HTML)

            logger.info('Бот ответил\n"{}"'.format(msg.text), user_id=call.message.chat.id)

        except ValueError as VE:
            logger.error("Произошла ошибка:\n{}".format(VE), user_id=call.message.chat.id)

            await bot.send_message(
                chat_id=administrators["Никита"],
                text="Произошла ошибка в функции date_choice_keyboard_callback_this_week "
                "у пользователя {id}\n"
                "\n"
                "{exec}".format(id=call.message.chat.id, exec=VE),
            )

            msg = await bot.send_message(
                chat_id=call.message.chat.id,
                text="К сожалению, расписания на текущую неделю пока нет. Ожидаем "
                "информацию от Храма. Сделаем уведомление, когда расписание будет "
                "загружено. Спасибо, что пользуетесь нашим Ботом {}".format(
                    emoji.emojize(":upside_down_face:", language="alias")
                ),
            )

        except Exception as Exec:
            logger.error("Произошла ошибка:\n{}".format(Exec), user_id=call.message.chat.id)

            await bot.send_message(
                chat_id=administrators["Никита"],
                text="Произошла ошибка в функции date_choice_keyboard_callback_this_week "
                "у пользователя {id} {name} {f_name} {username}\n"
                "\n"
                "{exec}".format(
                    id=call.message.chat.id,
                    name=call.message.from_user.first_name,
                    f_name=call.message.from_user.last_name,
                    username=call.message.from_user.username,
                    exec=Exec,
                ),
            )

            await bot.send_message(
                chat_id=call.message.chat.id,
                text="Приносим извинения, возникла непредвиденная ошибка. "
                "Технические специалисты уже работают над решением проблемы",
            )

    if call.data == "file_schedule_this":
        await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.UPLOAD_PHOTO)

        this_week_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%U"))

        if os.path.exists(schedule_photo_week_dir + week_photo_name.format(number=this_week_digit)):
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=open(schedule_photo_week_dir + week_photo_name.format(number=this_week_digit), "rb"),
            )

            logger.info("Бот отправил фото week_{}.jpg".format(this_week_digit), user_id=call.message.chat.id)

        else:
            msg = await bot.send_message(
                chat_id=call.message.chat.id,
                text="К сожалению, расписания на текущую неделю в виде файла пока нет. "
                "Ожидаем информацию от Храма. Сделаем уведомление, когда расписание "
                "будет загружено. Спасибо, что пользуетесь нашим Ботом {}".format(
                    emoji.emojize(":upside_down_face:", language="alias")
                ),
                parse_mode=ParseMode.HTML,
            )

            logger.info('Бот ответил "{}"'.format(msg.text), user_id=call.message.chat.id)

    elif call.data == "return_this":
        msg = await bot.edit_message_text(
            text="Вы хотите уточнить расписание богослужений",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_schedule_option(),
        )

        logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text), user_id=call.message.chat.id)

    else:

        msg = await bot.edit_message_text(
            text="Вы хотели посмотреть расписание на текущую неделю\n"
            "<i>- <code>Вы выбрали {button}</code></i>".format(button=button_text(call)),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_open_schedule(),
            parse_mode=ParseMode.HTML,
        )

        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text), user_id=call.message.chat.id)

        await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.TYPING)


############################################
"""
Отправка расписания на следующую неделю
"""


@dp.callback_query_handler(
    lambda call: call.message.content_type == "text"
    and call.message.text.startswith("Вы хотели посмотреть расписание на следующую неделю")
    and call.data != "open_again"
)
async def date_choice_keyboard_callback_next_week(call: CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Это для меню на неделю
    """
    logger.info(
        "Запущена функция date_choice_keyboard_callback_next_week, "
        'пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    if call.data == "text_schedule_next":

        await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.TYPING)

        try:
            day = datetime.datetime.now(pytz.timezone("Europe/Moscow"))

            if day.weekday() == 0:
                day += datetime.timedelta(weeks=1)
            else:
                while day.weekday() != 0:  # 0 for monday
                    day += datetime.timedelta(days=1)

            today_digit = day.strftime("%d")
            month_digit = int(day.strftime("%m"))

            next_monday = "{day} {month}".format(day=today_digit, month=all_months_in_calendar[month_digit - 1])

            days_till_week_end = 7

            all_days_in_schedule = [i for i in data_from_json(schedules_excel_dir + json_days_list) if i != "-"]

            next_mon = all_days_in_schedule.index(next_monday)

            all_week = all_days_in_schedule[next_mon : next_mon + days_till_week_end]

            await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.TYPING)

            week_schedule = schedule_for_some_days(
                days=all_week,
                username=call.message.from_user.username,
                user_id=call.message.chat.id,
            )

            msg = await bot.send_message(chat_id=call.message.chat.id, text=week_schedule, parse_mode=ParseMode.HTML)

            logger.info('Бот ответил\n"{}"'.format(msg.text), user_id=call.message.chat.id)
        except ValueError as VE:
            logger.error("Произошла ошибка:\n{}".format(VE), user_id=call.message.chat.id)

            await bot.send_message(
                chat_id=administrators["Никита"],
                text="Произошла ошибка в функции day_choice_keyboard_callback "
                "у пользователя {id}\n"
                "\n"
                "{exec}".format(id=call.message.chat.id, exec=VE),
            )

            msg = await bot.send_message(
                chat_id=call.message.chat.id,
                text="К сожалению, расписания на следующую неделю пока нет. Ожидаем "
                "информацию от Храма. Сделаем уведомление, когда расписание будет "
                "загружено. Спасибо, что пользуетесь нашим Ботом {}".format(
                    emoji.emojize(":upside_down_face:", language="alias")
                ),
            )

        except Exception as Exec:
            logger.error("Произошла ошибка:\n{}".format(Exec), user_id=call.message.chat.id)

            await bot.send_message(
                chat_id=administrators["Никита"],
                text="Произошла ошибка в функции date_choice_keyboard_callback_next_week "
                "у пользователя {id} {name} {f_name} {username}\n"
                "\n"
                "{exec}".format(
                    id=call.message.chat.id,
                    name=call.message.from_user.first_name,
                    f_name=call.message.from_user.last_name,
                    username=call.message.from_user.username,
                    exec=Exec,
                ),
            )

            await bot.send_message(
                chat_id=call.message.chat.id,
                text="Приносим извинения, возникла непредвиденная ошибка. Технические специалисты "
                "уже работают над решением проблемы",
            )

    if call.data == "file_schedule_next":
        await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.UPLOAD_PHOTO)

        next_week_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%U")) + 1

        if os.path.exists(schedule_photo_week_dir + week_photo_name.format(number=next_week_digit)):
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=open(schedule_photo_week_dir + week_photo_name.format(number=next_week_digit), "rb"),
            )

            logger.info("Бот отправил фото week_{}.jpg".format(next_week_digit), user_id=call.message.chat.id)

        else:
            msg = await bot.send_message(
                chat_id=call.message.chat.id,
                text="К сожалению, расписания на следующую неделю в виде файла пока нет. "
                "Ожидаем информацию от Храма. Сделаем уведомление, когда расписание "
                "будет загружено. Спасибо, что пользуетесь нашим Ботом {}".format(
                    emoji.emojize(":upside_down_face:", language="alias")
                ),
                parse_mode=ParseMode.HTML,
            )

            logger.info('Бот ответил "{}"'.format(msg.text), user_id=call.message.chat.id)

    elif call.data == "return_next":
        msg = await bot.edit_message_text(
            text="Вы хотите уточнить расписание богослужений",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_schedule_option(),
        )

        logger.info('Бот отредактировал сообщение и написал "{}"'.format(msg.text), user_id=call.message.chat.id)

    else:

        msg = await bot.edit_message_text(
            text="Вы хотели посмотреть расписание на следующую неделю\n"
            "<i>- <code>Вы выбрали {button}</code></i>".format(button=button_text(call)),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_open_schedule(),
            parse_mode=ParseMode.HTML,
        )

        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text), user_id=call.message.chat.id)

        await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.TYPING)


############################################
"""
Отправка расписания на месяц
"""


@dp.callback_query_handler(
    lambda call: call.message.content_type == "text"
    and call.message.text.startswith("Вы хотите уточнить расписание богослужений")
    and call.data == "month"
)
async def month_choice_keyboard_callback(call: CallbackQuery) -> None:
    """
    Обработчик нажатия на клавиатуру с выбором даты. Выбран пункт "Месяц"
    """

    logger.info(
        'Запущена функция month_choice_keyboard_callback пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    await bot.send_chat_action(chat_id=call.message.chat.id, action=ChatActions.UPLOAD_PHOTO)

    this_month_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%m"))

    current_month = all_months_in_calendar_for_save[this_month_digit - 1]
    year_digit = int(datetime.datetime.now(pytz.timezone("Europe/Moscow")).strftime("%Y"))

    try:
        await bot.send_document(
            chat_id=call.message.chat.id,
            document=open(
                schedule_photo_month_dir + month_photo_name.format(month=current_month, year=year_digit), "rb"
            ),
        )

        logger.info("Бот отправил файл {}.pdf".format(current_month), user_id=call.message.chat.id)

    except FileNotFoundError:
        msg = await bot.send_message(
            chat_id=call.message.chat.id,
            text="К сожалению, расписания на весь месяц в виде файла пока нет. "
            "Ожидаем информацию от Храма. Сделаем уведомление, когда расписание "
            "будет загружено. Спасибо, что пользуетесь нашим Ботом {}".format(
                emoji.emojize(":upside_down_face:", language="alias")
            ),
            parse_mode=ParseMode.HTML,
        )

        logger.info('Бот ответил "{}"'.format(msg.text), user_id=call.message.chat.id)


############################################
"""
Кнопка открыть меню
"""


@dp.callback_query_handler(lambda call: call.data == "open_again")
async def date_open_keyboard_callback(call: CallbackQuery) -> None:
    """
    Обработчик нажатия на кнопку "Открыть меню" для повторного выбора дня и расписания
    """

    logger.info(
        "Запущена функция date_open_keyboard_callback, " 'пользователь нажал на кнопку "{}"'.format(button_text(call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id,
    )

    if "На какой день Вы хотели посмотреть расписание?" in call.message.text:
        all_days_in_schedule = [i for i in data_from_json(schedules_excel_dir + json_days_list) if i != "-"]

        msg = await bot.edit_message_text(
            text="На какой день Вы хотели посмотреть расписание?",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_date_schedule_choice(days_list=all_days_in_schedule),
        )

        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text), user_id=call.message.chat.id)

    elif "Вы хотели посмотреть расписание на текущую неделю" in call.message.text:
        msg = await bot.edit_message_text(
            text="Вы хотели посмотреть расписание на текущую неделю. Выберите удобный вариант",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_week_schedule_choice_1(),
        )

        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text), user_id=call.message.chat.id)

    elif "Вы хотели посмотреть расписание на следующую неделю" in call.message.text:
        msg = await bot.edit_message_text(
            text="Вы хотели посмотреть расписание на следующую неделю. Выберите удобный вариант",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=IKM_week_schedule_choice_2(),
        )

        logger.info('Бот отредактировал сообщение и написал\n"{}"'.format(msg.text), user_id=call.message.chat.id)
