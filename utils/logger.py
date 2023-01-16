# import datetime
import logging

from loader import log_dir, log_file_name


class CustomAdapter(logging.LoggerAdapter):
    """
    Класс, который позволяет иметь логгеру динамический атрибут. По умолчанию никнейм и id Пользователя определены как
    None, но когда мы ведем журнал событий, то можем переопределить их исходя уже из информации о конкретном
    Пользователе
    """
    
    def process(self, log_message: str, user_dict_info: dict) -> tuple:
        """
        Функция, которая добавляет нужную информацию о Пользователе в строку журнала событий
        :param log_message: Само сообщение журнала событий
        :type log_message: str
        :param user_dict_info: Словарь, с информацией о никнейме и id Пользователя
        :type user_dict_info: dict
        
        :return: Возвращается дополненное информацией о Пользователе сообщение логгера
        :rtype: tuple
        """
        
        username = user_dict_info.pop('username', self.extra['username'])
        # first_name = user_dict_info.pop('username', self.extra['firstname'])
        # last_name = user_dict_info.pop('username', self.extra['lastname'])
        user_id = user_dict_info.pop('user_id', self.extra['user_id'])
        
        return '[username %s] - ' \
               '[user_id %s] - ' \
               '[%s]' % (username, user_id, log_message), user_dict_info


# logging.basicConfig(filename='./hdd/logs/{year}-{month}-{day} bot_detail.log'.format(
#     year=datetime.datetime.now().strftime("%Y"),
#     month=datetime.datetime.now().strftime("%m"),
#     day=datetime.datetime.now().strftime("%d")
# ),
logging.basicConfig(filename=log_dir + log_file_name,
                    level=logging.INFO,
                    encoding='utf-8',
                    format='[%(levelname)s] - '
                           '[%(asctime)s] - '
                           '[file %(filename)s] - '
                           '[func %(funcName)s] - '
                           '[num_string %(lineno)d] - '
                           '%(message)s'
                    )

logger = logging.getLogger('logger')
log_main = logging.getLogger('log_main')
logger = CustomAdapter(logger, {'username': 'system',
                                'user_id': 'system'})
