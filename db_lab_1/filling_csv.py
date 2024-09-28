import psycopg2
import random
import datetime
from faker import Faker

COUNT = 1000  # количество строк таблицы, которое хотим заполнить
path_to_data = 'C:\data_db\\'


def author_filling():
    fake = Faker()
    # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
    table_name = "author"
    column_names = ', '.join(('id_author', 'first_name', 'last_name', 'birth_year', 'death_year'))

    with open(f"{path_to_data}{table_name}.csv", "w") as f:
        for i in range(COUNT):
            # birth = fake.date_of_birth(minimum_age=0, maximum_age=2000)
            birth = random.randint(0, 2000)
            death = random.randint(birth + 1, 2024)
            vals = "{0};{1};{2};{3};{4}\n".format(i, fake.first_name(), fake.last_name(), birth, death)

            f.write(vals)


def artwork_filling():
    fake = Faker()
    table_name = "artwork"
    column_names = ', '.join(('id_artwork', 'name', 'style', 'year_create', 'format', 'id_author'))

    with open(f"{path_to_data}{table_name}.csv", "w") as f:
        for i in range(COUNT):
            vals = "{0};{1};{2};{3};{4};{5}\n".format(i, fake.word(), fake.word(), fake.year(), fake.word(), random.randint(0, COUNT - 1))

            f.write(vals)

# def author_artwork_filling():
#     table_name = "author_artwork"
#     column_names = ', '.join(('id_author', 'id_artwork'))
#
#     k = 3
#     with open(f"{path_to_data}{table_name}.csv", "w") as f:
#         for i in range(0, COUNT):
#             for j in range(0, random.randint(1, k)):
#                 vals = "{0};{1}\n".format(i, random.randint(0, COUNT - 1))
#             f.write(vals)


def owner_of_artwork_filling():
    fake = Faker()
    # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
    table_name = "owner_of_artwork"
    column_names = ', '.join(('id_owner_of_artwork', 'first_name', 'last_name', 'phone', 'adress'))

    with open(f"{path_to_data}{table_name}.csv", "w") as f:
        for i in range(COUNT):
            vals = "{0};{1};{2};{3};{4}\n".format(i, fake.word(), fake.year(), fake.phone_number(), fake.address().replace('\n', ' '))

            f.write(vals)


def history_of_ownership_artwork_filling():
    fake = Faker()
    table_name = "history_of_ownership_artwork"
    column_names = ', '.join(('id_owner_of_artwork', 'id_artwork'))

    k = 3
    with open(f"{path_to_data}{table_name}.csv", "w") as f:
        for i in range(0, COUNT):
            for j in range(0, random.randint(1, k)):
                purchase = fake.date_object()
                sale = fake.date_between(purchase)
                vals = "{0};{1};{2};{3}\n".format(i, random.randint(0, COUNT - 1), purchase, sale)
                f.write(vals)

                purchase = fake.date_object()
                sale = fake.date_between(purchase)
                vals = "{0};{1};{2};{3}\n".format(random.randint(0, COUNT - 1), i, purchase, sale)
                f.write(vals)


def exhibition_filling():
    fake = Faker()
    # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
    table_name = "exhibition"
    column_names = ', '.join(('id_exhibition', 'title', 'begin_date', 'end_date', 'adress'))

    with open(f"{path_to_data}{table_name}.csv", "w") as f:
        for i in range(0, COUNT):
            begin = fake.date_object()
            end = fake.date_between(begin)
            vals = "{0};{1};{2};{3};{4}\n".format(i, fake.word(), begin, end, fake.address().replace('\n', ' '))
            f.write(vals)


def history_exhibition_filling():
    # INSERT INTO author (id_author, first_name, last_name, birth_year, death_year) VALUES (1, 'qwe', 'wer', 2000, 2020)
    table_name = "history_exhibition"
    column_names = ', '.join(('id_artwork', 'id_exhibition'))

    k = 3
    with open(f"{path_to_data}{table_name}.csv", "w") as f:
        for i in range(0, COUNT):
            for j in range(0, random.randint(1, k)):
                vals = "{0};{1}\n".format(i, random.randint(0, COUNT - 1))
            for j in range(0, random.randint(1, k)):
                vals = "{0};{1}\n".format(random.randint(0, COUNT - 1), i)
            f.write(vals)


if __name__ == '__main__':
    author_filling()
    artwork_filling()
    # author_artwork_filling()
    owner_of_artwork_filling()
    history_of_ownership_artwork_filling()
    exhibition_filling()
    history_exhibition_filling()
