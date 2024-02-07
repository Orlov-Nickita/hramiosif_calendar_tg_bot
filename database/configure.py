from sqlalchemy import create_engine, MetaData, Table
from database.db import DataBase
from loader import PG_USER, PG_PASS, PG_HOST, PG_PORT, PG_NAME

engine = create_engine(
    f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_NAME}"
)
meta = MetaData(engine)

table_bot_users = Table("bot_users", meta, autoload=True)
table_admin_hdd_roots = Table("admin_hdd_roots", meta, autoload=True)

db = DataBase(engine, table_bot_users=table_bot_users, table_admin_hdd_roots=table_admin_hdd_roots)
