import telebot
from keyboards_for_bot.admin_keyboards import IKM_admin_check_hdd
from loader import bot
from utils.logger import logger

# check_func()


def start(message: telebot.types.Message) -> None:
    """
    Функция проверки состояния жесткого диска.
    :param message: Принимается сообщение от пользователя.
    :return: Возвращается приветственное сообщение и открывается меню бота с клавиатурой.
    """
    logger.info('Запущена функция admin_hdd_check.start',
                username=message.chat.username,
                user_id=message.chat.id)
    
    # for root, dirs, files in os.walk("."):
    #     print(root, dirs, files)
    
    files = []
    
    # for i in os.listdir('./hdd/'):
        # print(os.path.abspath(i))
        # if os.path.isdir(i):
            # print('Папка', i)
        # else:
            # print('Файл', i)
        # files.append(i)
    
    bot.send_message(chat_id=message.chat.id,
                     text='Список файлов',
                     reply_markup=IKM_admin_check_hdd(files))


@bot.callback_query_handler(func=lambda call: True and 'Список файлов' in call.message.text)
def save_schedule_to_the_week(call: telebot.types.CallbackQuery) -> None:
    pass
    # print(call.data)
    # print(os.path.isdir(call.data))
    # print(os.path.abspath('./') + 'hdd')
    # print(os.path.abspath(os.path.join(os.path.sep)))
    
    # os.chdir()
    
    # if call.data == 'logs':
        # os.chdir('../')
        # print(os.getcwd())
