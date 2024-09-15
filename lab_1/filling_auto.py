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


if __name__ == '__main__':
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

    # artwork_filling()

# import random
# import datetime
# from faker import Faker
# from faker.providers.address.ru_RU import Provider
#
# COUNT = 100  # количество строк таблицы, которое хотим заполнить
#
#
# # Создание объекта Faker с локализацией для России
# # fake = Faker()
# # fake.add_provider(Provider)
#
#
# def author_filling():
#     fake = Faker()
#     # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
#     table_name = "author"
#     column_names = ', '.join(('id_author', 'first_name', 'last_name', 'birth_year', 'death_year'))
#
#     filename = f'{table_name}_filling.sql'
#     with open(filename, 'w') as f:
#         f.write('DELETE FROM author;')
#         for i in range(COUNT):
#             birth = fake.date_of_birth(minimum_age=0, maximum_age=2000)
#             vals = f"{i}, '{fake.first_name()}', '{fake.last_name()}', {birth.year}, NULL"
#
#             query = f"INSERT INTO {table_name} ({column_names}) VALUES ({vals});\n"
#             f.write(query)
#
#
# def artwork_filling():
#     table_name = 'artwork'
#     column_names = ('id_artwork', 'style', 'year_create', 'id_author')
#
#     filename = f'{table_name}_filling.sql'
#     with open(filename, 'w') as f:
#         columns_str = ', '.join(f'"{column}"' for column in column_names)
#         for i in range(COUNT):
#             values = [i + 1, fake.word(), fake.year(), random.randint(0, COUNT)]
#             values_str = ', '.join(str(value) for value in values)
#             insert_query = f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({values_str});\n'
#             print(insert_query)
#             f.write(insert_query)
#         f.close()
#
#
# if __name__ == '__main__':
#     author_filling()
#     # artwork_filling()
