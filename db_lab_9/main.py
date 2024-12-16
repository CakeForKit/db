
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db_work import *
from actions import *

from times import times_select, times_insert, times_delete




if __name__ == '__main__':
    connection = connect()
    # engine = create_engine(
    #             f'postgresql://{DB_SETTINGS["user"]}:{DB_SETTINGS["password"]}@{DB_SETTINGS["host"]}:{DB_SETTINGS["port"]}/{DB_SETTINGS["name"]}',
    #             pool_pre_ping=True)
    r = redis.Redis()
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # res = get_top_categories(connection, 10)
    # r.flushdb()
    # res = get_top_categories_cache(connection, r)
    # print(res)

    # res = add_artwork(connection, r)
    # print(res)
    # session.commit()

    # times_select(connection, r)
    times_insert(connection, r)
    # times_delete(connection, r)