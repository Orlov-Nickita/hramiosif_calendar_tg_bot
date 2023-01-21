from html.parser import HTMLParser

class HTMLFilter(HTMLParser):
    """
    Класс для подготовки текста к удалению HTML тэгов
    """
    text = ""
    
    def handle_data(self, data):
        self.text += data


def html_to_text_parser(text: str) -> str:
    """
    Функция удаления HTML тэгов из текста для привидения в читаемый вид
    """
    temp = HTMLFilter()
    temp.feed(text)
    return temp.text

