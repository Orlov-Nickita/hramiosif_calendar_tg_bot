"""
Модуль с функциями для работы с текстом HTML
"""

from html.parser import HTMLParser


class HTMLFilter(HTMLParser):
    """
    Класс для подготовки текста к удалению HTML тэгов
    """

    text = ""

    def handle_data(self, data):
        """
        Метод для формирования текста
        """
        self.text += data


def html_to_text_parser(text: str) -> str:
    """
    Функция удаления HTML тэгов из текста для привидения в читаемый вид
    """
    temp = HTMLFilter()
    temp.feed(text)
    return temp.text
