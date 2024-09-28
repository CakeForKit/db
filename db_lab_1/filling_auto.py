import psycopg2
import random
import datetime
from faker import Faker
from faker.providers.address.ru_RU import Provider

COUNT = 1000  # количество строк таблицы, которое хотим заполнить


def author_filling():
    fake = Faker()
    # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
    table_name = "author"
    column_names = ', '.join(('id_author', 'first_name', 'last_name', 'birth_year', 'death_year'))

    query = 'DELETE FROM author;\n'
    for i in range(COUNT):
        birth = fake.date_of_birth(minimum_age=0, maximum_age=2000)
        vals = f"{i}, '{fake.first_name()}', '{fake.last_name()}', {birth.year}, NULL"

        query += f"INSERT INTO {table_name} ({column_names}) VALUES ({vals});\n"

    return query


def artwork_filling():
    fake = Faker()
    # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
    table_name = "artwork"
    column_names = ', '.join(('id_artwork', 'style', 'year_create', 'id_author'))

    query = f'DELETE FROM {table_name};\n'
    for i in range(COUNT):
        vals = f"{i}, '{fake.word()}', '{fake.year()}', {random.randint(0, COUNT - 1)}"

        query += f"INSERT INTO {table_name} ({column_names}) VALUES ({vals});\n"

    return query

def owner_of_artwork_filling():
    fake = Faker()
    # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
    table_name = "owner_of_artwork"
    column_names = ', '.join(('id_owner_of_artwork', 'first_name', 'last_name'))

    query = f'DELETE FROM {table_name};\n'
    for i in range(COUNT):
        vals = f"{i}, '{fake.first_name()}', '{fake.last_name()}'"

        query += f"INSERT INTO {table_name} ({column_names}) VALUES ({vals});\n"

    return query

def owner_of_artworkship_history_filling():
    fake = Faker()
    # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
    table_name = "owner_of_artworkship_history"
    column_names = ', '.join(('id_owner_of_artwork', 'id_artwork'))

    query = f'DELETE FROM {table_name};\n'
    for i in range(COUNT):
        vals = f"{i}, {random.randint(0, COUNT - 1)}"

        query += f"INSERT INTO {table_name} ({column_names}) VALUES ({vals});\n"

    return query

def exhibition_filling():
    fake = Faker()
    # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
    table_name = "exhibition"
    column_names = ', '.join(('id_exhibition', 'title', 'begin_date', 'end_date', 'adress'))

    query = f'DELETE FROM {table_name};\n'
    for i in range(COUNT):
        begin = random.randint(0, 2024)
        end = random.randint(begin + 1, 2024)
        vals = f"{i}, '{fake.word()}', '{begin}', '{end}', '{fake.address()}'"

        query += f"INSERT INTO {table_name} ({column_names}) VALUES ({vals});\n"

    return query

def filling():
    conn = psycopg2.connect(dbname='works_of_art', host='localhost', user='postgres', password='163785303')
    with conn.cursor() as cursor:
        # query = 'SELECT * FROM author'
        query = author_filling()
        query += artwork_filling()
        query += owner_of_artwork_filling()
        query += owner_of_artworkship_history_filling()
        query += exhibition_filling()
        cursor.execute(query)
        # record = cursor.fetchall()
        # print(record)
        conn.commit()
    conn.close()


def history_exhibition_adding():
    conn = psycopg2.connect(dbname='works_of_art', host='localhost', user='postgres', password='163785303')
    with conn.cursor() as cursor:

        table_name = "history_exhibition"
        column_names = ', '.join(('id_artwork', 'id_exhibition'))

        # Получить результат
        cursor.execute(f"SELECT count(*) from {table_name}")
        len_history_exhibition = cursor.fetchall()[0][0]
        cursor.execute(f"SELECT count(*) from artwork")
        len_artwork = cursor.fetchall()[0][0]
        cursor.execute(f"SELECT count(*) from exhibition")
        len_exhibition = cursor.fetchall()[0][0]
        print(f'len_history_exhibition = {len_history_exhibition}\n'
              f'len_artwork = {len_artwork}\n'
              f'len_exhibition = {len_exhibition}')

        query = ''
        count_add = 500
        i = len_history_exhibition + 1
        for exh_i in [random.randint(0, len_exhibition) for i in range(count_add)]:
            art_i = random.randint(0, len_artwork)

            query += f"INSERT INTO {table_name} ({column_names}) VALUES ({art_i}, {exh_i});\n"

        print(query)
        cursor.execute(query)

        conn.commit()

    conn.close()


if __name__ == '__main__':
    history_exhibition_adding()

