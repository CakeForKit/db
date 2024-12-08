import psycopg2

TABLE_CREATED = False
DB_SETTINGS = {
    "dbname": "postgres",
    "host": "localhost",
    "user": "postgres",
    "password": "163785303"
    # "port": 5432
}

def scalar_query():
    print("Скалярный запрос.\nПолучить жанры произведений искусства которые были написаны творцами 20 века\n")
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''  select style
                                    from artwork
                                    where id_author in (select id_author
                                                        from author
                                                        where birth_year >= 1900 and death_year < 2000);''')
                result = cursor.fetchall()
                print("Жанры: " + ', '.join(elem[0] for elem in result))
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

def join_query():
    print("Запрос с несколькими соединениями (JOIN).\n"
          "Получить выставки на которых присутствуют работы автора с id_artwork = 1\n")
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''select e.id_exhibition -- , e.title -- , art.id_artwork
                                    from exhibition e
                                    join history_exhibition he
                                    on e.id_exhibition = he.id_exhibition
                                    join artwork art
                                    on art.id_artwork = he.id_artwork
                                    where art.id_artwork = 1''')
                result = cursor.fetchall()
                print("id_exhibition: " + ', '.join(str(elem[0]) for elem in result))
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

def otv_query():
    print("Запрос с ОТВ и оконными функциями..\n"
          "Получить данные о выставках с максимальный количеством работ\n")
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''with exh_group as (
                                            select id_exhibition, count(*) as count_artwork
                                            from history_exhibition
                                            group by id_exhibition
                                        )
                                        select id_exhibition
                                        from exh_group
                                        where count_artwork = (	select max(count_artwork)
                                                                from exh_group
                                                                )''')
                result = cursor.fetchall()
                print("id_exhibition: " + ', '.join(str(elem[0]) for elem in result))
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")


def meta_query():
    print("Запрос к метаданным.")
    print("Выводит названия таблиц, их столбцы и типы в схеме public.\n")
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''select t.table_name, c.column_name, c.data_type 
                                    from information_schema.tables t
                                    join information_schema.columns c on t.table_name = c.table_name
                                    where t.table_schema = 'public'
                                    order by t.table_name, c.column_name''')

                print(', '.join(['table_name', 'column_name', 'data_type']))
                for line in cursor.fetchall():
                    print(line)

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

def call_scalar_function():
    print("Вызывает скалярную функцию.")
    print("Получить максимальное количество работ принадлежащих одному автору.\n")
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''select max_count_work_one_author() as max_work_one_author;''')
                m = cursor.fetchone()[0]
                print(f'Максимальное количество работ принадлежащих одному автору: {m}')

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")


def call_multi_operator_function():
    print("Вызывает многооператорную функцию.")
    print("Получить данные о выставках с максимальный количеством работ.\n")
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''select * from max_count_works();''')
                result = cursor.fetchall()
                print("id_exhibition: " + ', '.join(str(elem[0]) for elem in result))

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

def call_procedure():
    date = '2024-09-01'
    plus_days = 1
    print("Вызывает хранимую процедуру.")
    print(f"Продлить все выставки начавшиеся после {date} на {plus_days} дней")
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''call extend_exhibitions('{date}', {plus_days});''')
                print('Процедура была вызвана')

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

def call_system_function():
    try:
        print("Вызывает системную функцию now().\n")
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute("select now();")
                current_time = cursor.fetchone()[0]
                print(f"Текущее время: {current_time}")

    except Exception as e:
        print(f"Ошибка при вызове: {e}")

def create_table():
    global TABLE_CREATED
    print(f"Создает таблицу public.tmp_arwork")
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''create table if not exists public.tmp_arwork (
                                                    id serial not null,
                                                    name_art varchar(100),
                                                    primary key(id),
                                                    yg jsonb
                                                );''')

                print(f"Таблица создана")
                TABLE_CREATED = True
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

def insert_into_table():
    global TABLE_CREATED
    if not TABLE_CREATED:
        print('Ошибка. Сначала создайте таблицу (пункт 9)\n')
        return

    print(f"Выполняет вставку данных в созданную таблицу с использованием инструкции INSERT.")
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''insert into public.tmp_arwork (name_art, yg) 
                                values ('The Fighting Temeraire', '{"genre": "Impressionism", "year": 1839}'),
                                       ('Dance at Le Moulin de la Galette', '{"genre": "Impressionism", "year": 1876}'),
                                       ('Le Premier Disque', '{"genre": "Abstract", "year": 1912}');''')

                print(f"Данные добавлены")
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")


def exit_program():
    with psycopg2.connect(**DB_SETTINGS) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''drop table if exists public.tmp_arwork;''')

    print("Программа завершена.")
    exit()

def menu():
    actions = {
        0: exit_program,
        1: scalar_query,
        2: join_query,
        3: otv_query,
        4: meta_query,
        5: call_scalar_function,
        6: call_multi_operator_function,
        7: call_procedure,
        8: call_system_function,
        9: create_table,
        10: insert_into_table
    }

    while True:
        print("""
Меню:
1. Выполнить скалярный запрос
2. Выполнить запрос с несколькими соединениями (JOIN)
3. Выполнить запрос с ОТВ(CTE) и оконными функциями
4. Выполнить запрос к метаданным
5. Вызвать скалярную функцию
6. Вызвать многооператорную функцию
7. Вызвать хранимую процедуру
8. Вызвать системную функцию или процедуру
9. Создать таблицу в базе данных
10. Выполнить вставку данных в созданную таблицу с использованием инструкцию INSERT
0. Выйти
        """)

        try:
            act = int(input("Введите действие: "))
            if act in actions:
                actions[act]()
            else:
                print("Ошибка. Такого действия пока нет.")
        except ValueError:
            print("Ошибка. Введите число.")


if __name__ == '__main__':
    menu()