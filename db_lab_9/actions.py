
from db_work import *
import datetime
from faker import Faker
import random

CACHE_KEY = "cache"

QUERY_TOP_AUTHORS = '''select id_author, count(*) as cnt
                        from artwork
                        group by id_author
                        order by cnt desc'''


def get_top_authors(connection):
    data = "Top authors: "
    cursor = execute_query(connection, QUERY_TOP_AUTHORS)
    if cursor is not None:
        res = cursor.fetchall()
        for category in res:
            data += str(category[0]) + ", "
        data = data.rstrip(", ")

    return data

def get_top_authors_cache(connection, r):
    data = "Top Categories: "
    redis_cache = r.get(CACHE_KEY)
    if redis_cache is not None:
        print("DATA FROM CACHE")
        return redis_cache.decode("utf-8")
    else:
        # return "NO DATA IN CACHE"
        print("NO DATA IN CACHE")
        cursor = execute_query(connection, QUERY_TOP_AUTHORS)
        if cursor is not None:
            res = cursor.fetchall()
            for category in res:
                data += str(category[0]) + ", "
            data = data.rstrip(", ")

        r.set(CACHE_KEY, data)

        return data
    


def add_artwork(connection, r):
    max_id_author = execute_query(connection, 'select count(*) from author').fetchall()[0][0] - 1
    id_artwork = execute_query(connection, 'select count(*) from artwork').fetchall()[0][0]

    fake = Faker()
    query = f'''insert into artwork(id_artwork, name, style, year_create, format, id_author)
                            values ({id_artwork}, '{fake.word()}', '{fake.word()}', 
                            '{fake.year()}', '{fake.word}', '{random.randint(0, max_id_author)}')
                            returning id_artwork;'''
    res = execute_query(connection, query)
    r.expire(CACHE_KEY, datetime.timedelta(seconds=0))
    connection.commit()

    return f'add to artwork id = {res.fetchall()[0][0]}'


def delete_artwork(connection, r):
    id_artwork = execute_query(connection, 'select count(*) from artwork').fetchall()[0][0] - 1

    query = f'''delete from artwork
                where id_artwork = {id_artwork}
                returning id_artwork;'''
    res = execute_query(connection, query)
    r.expire(CACHE_KEY, datetime.timedelta(seconds=0))
    connection.commit()
    
    return f'delete from artwork id = {res.fetchall()[0][0]}'