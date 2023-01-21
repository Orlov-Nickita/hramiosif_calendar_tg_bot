from typing import List


class Photo_album:
    """
    Класс для модификации обычного списка и создания из него итерируемого объекта и в одну сторону и в другую,
    как фотоальбом. При выводе на печать, выводится самый первый элемент из списка, используя соответствующие методы,
    можно выбирать следующий элемент списка или предыдущий
    """
    
    def __init__(self, mylist: List) -> None:
        self.i_list = mylist
    
    def next(self) -> List:
        self.i_list = self.i_list[1:] + self.i_list[:1]
        return self.i_list[0]
    
    def prev(self) -> List:
        self.i_list = self.i_list[-1:] + self.i_list[:-1]
        return self.i_list[0]
    
    def show(self):
        return self.i_list[0]
