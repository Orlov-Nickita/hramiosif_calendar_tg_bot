"""
Модуль обработки админ команды на отправку документации
"""

from aiogram.types import Message, ChatActions, ParseMode
from loader import bot, qr_code_dir, qr_code
from utils.logger import logger


async def send_qrcode(message: Message) -> None:
    """
    Функция для получения фото с qr-кодом.
    :param message: Сообщение от пользователя.
    :return: Файл с qr-кодоом.
    """
    logger.info('Запущена функция send_qrcode',
                username=message.chat.username,
                user_id=message.chat.id)
    
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.UPLOAD_DOCUMENT)

    msg = """
<b><u>Дорогие братья и сестры!</u></b>

Храм нуждается в помощи по оплате коммунальных услуг.
В отопительный сезон сумма оплаты доходит до 100.000 в месяц.

Желающие оказать помощь могут обратиться по телефону: <code>+79637723411</code> <u>Отец Петр</u>

<b>Реквизиты храма для перечисления пожертвований:</b>
<i>Полное наименование:</i> <code>Местная религиозная организация православный приход Иосифо-Волоцкого храма п. Развилка Ленинского района Московской области Московской епархии Русской Православной Церкви</code>
<i>ИНН:</i> <code>5003032803</code>
<i>КПП:</i> <code>500301001</code>
<i>ОГРН:</i> <code>1035000030977</code>
<i>ОКВЭД:</i> <code>94.91</code> 
<i>ОКПО:</i> <code>48796267</code> 
<i>ОКТМО:</i> <code>46628416</code>
<i>БИК:</i> <code>044525225</code> 
<i>Р/сч:</i> <code>40703810940000001877</code> 
<i>Кор/сч:</i> <code>30101810400000000225 Доп.офис №9040/00233 Видновское отделение Среднерусского банка ПАО «Сбербанк» России</code>

Для возможности быстрого перевода пожертвований на ремонт и нужды Иосифо-Волоцкого храма оформлен QR код в Сбербанке.
Наведя на него камеру смартфона вы можете быстро оформить перевод пожертвований:
    """

    await bot.send_message(chat_id=message.chat.id, text=msg, parse_mode=ParseMode.HTML)
    await bot.send_photo(chat_id=message.chat.id, photo=open(qr_code_dir + qr_code, 'rb'))

    logger.info('Бот отправил информацию о пожертвованиях', user_id=message.chat.id)
