from typing import Dict, Union, List, Callable
from sqlalchemy import select
from sqlalchemy.engine import ResultProxy


class DataBase:
    """
    Класс для настройки работы с Базой данных
    """

    def __init__(self, engine, table_bot_users, table_admin_hdd_roots):
        self.engine = engine
        self.table_bot_users = table_bot_users
        self.table_admin_hdd_roots = table_admin_hdd_roots

    @staticmethod
    def __to_dict(
            model: ResultProxy, one: bool = False
    ) -> Union[List[Dict], Dict, bool]:
        """
        Преобразует полученные данные из базы данных в словарь с названиями полей в качестве ключей для удобства
        работы с данными. Параметр one используется для случаев, когда получаем одну запись из БД
        """
        columns = model.keys()
        model_dict = []

        if not one:
            for i_m in model.fetchall():
                model_dict.append(
                    dict(zip(columns, i_m))
                )
            return model_dict

        try:
            return dict(zip(columns, model.first()))
        except TypeError:
            return False

    def user_get_by_id(self, user_id: int):
        """
        Получаем запись из БД по ее ID
        """
        with self.engine.connect() as conn:
            user_raw: ResultProxy = conn.execute(
                select(self.table_bot_users)
                .where(self.table_bot_users.c.id == user_id)
            )
            return self.__to_dict(user_raw, one=True)

    def user_create(self, values: Dict) -> None:
        """
        Создаем запись
        """
        with self.engine.connect() as conn:
            conn.execute(
                self.table_bot_users
                .insert()
                .values(
                    **values
                )
            )

    def user_all_qty_in_db(self) -> Callable[[], int]:
        """
        Считает количество записей в БД
        """
        with self.engine.connect() as conn:
            user_raw: ResultProxy = conn.execute(
                select(self.table_bot_users)
            )
            return user_raw.rowcount

    def hdd_get_koren_or_path(self, user_id: int, is_koren: bool = False, is_path: bool = False) -> str:

        with self.engine.connect() as conn:
            hdd_raw: ResultProxy = conn.execute(
                select(self.table_admin_hdd_roots)
                .where(self.table_admin_hdd_roots.c.user_id == user_id)
            )
            hdd = self.__to_dict(hdd_raw, one=True)
            if is_path:
                res = hdd.get('path')
            elif is_koren:
                res = hdd.get('coren')
            else:
                raise TypeError

            return res

    def hdd_update_by_id(self, user_id: int, values: Dict):
        """
        Обновляем запись из БД по ее ID
        """
        with self.engine.connect() as conn:
            conn.execute(
                self.table_admin_hdd_roots
                .update()
                .where(self.table_admin_hdd_roots.c.user_id == user_id)
                .values(**values)
            )
