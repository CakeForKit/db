import redis
import json
import psycopg2
from datetime import datetime, date
from time import sleep, time
import random
import numpy as np
import matplotlib.pyplot as plt
from faker import Faker
import random

DB_SETTINGS = {
    "name": "postgres",
    "host": "localhost",
    "user": "root",
    "password": "postgres",
    "port": 5433
}
CACHE_KEY = 'top_authors'

QUERY = '''select id_author, count(*) as cnt
        from artwork
        group by id_author
        order by cnt desc'''

def dbconnect():
    connection = psycopg2.connect(
        user=DB_SETTINGS['user'],
        password=DB_SETTINGS['password'],
        host=DB_SETTINGS['host'],
        port=DB_SETTINGS['port'],
        database=DB_SETTINGS['name']
    )
    return connection

    
def print_top(data):
    print('top authors:')
    elem = ['id', 'count']
    print(f'{elem[0]:<5} {elem[1]:<5}')
    for elem in data:
        print(f'{elem[0]:<5} {elem[1]:<5}')
    print()

def get_top_authors(cur):
    r = redis.Redis()
    cache_value = r.get(CACHE_KEY)
    
    if cache_value is not None:
        r.close()
        return json.loads(cache_value)[:10]
    
    cur.execute(QUERY)
    results = cur.fetchall()
    
    r.set(CACHE_KEY, json.dumps(results, default=str))
    r.close()
    return results[:10]

def get_experiments_from_db(cur):
    cur.execute(QUERY)
    return cur.fetchall()[:10]

def get_experiments_from_redis(cur):
    r = redis.Redis()
    cache_value = r.get(CACHE_KEY)
    cur.execute(QUERY)
    res = cur.fetchall()
    data = json.dumps(res, default=str)
    r.set(CACHE_KEY, data)
    r.close()
    return res

def select_analis(cur):
    r = redis.Redis()
    t1 = time()
    cur.execute(QUERY)
    t2 = time()
    result = cur.fetchall()

    data = json.dumps(result, default=str)
    cache_value = r.get(CACHE_KEY)
    if cache_value is not None:
        pass
    else:
        r.set(CACHE_KEY, json.dumps(cache_value, default=str))
    t3 = time()
    r.get(CACHE_KEY)
    t4 = time()
    r.close()
    return t2 - t1, t4 - t3
    
def insert_analis(cur, conn):
    r = redis.Redis()
    
    max_id_author = cur.execute(conn, 'select count(*) from author').fetchall()[0][0] - 1
    id_artwork = cur.execute(conn, 'select count(*) from artwork').fetchall()[0][0]

    fake = Faker()
    query = f'''insert into artwork(id_artwork, name, style, year_create, format, id_author)
                            values ({id_artwork}, '{fake.word()}', '{fake.word()}', 
                            '{fake.year()}', '{fake.word}', '{random.randint(0, max_id_author)}');'''
    
    t1 = time()
    cur.execute(conn, query)
    t2 = time()
    conn.commit() 

    cur.execute(QUERY)
    results = cur.fetchall()
    print_top(results)
    
    data = json.dumps(results, default=str)
    t3 = time()
    r.set(CACHE_KEY, data)
    t4 = time()
    r.close()

    return t2 - t1, t4 - t3

def delete_analis(cur, conn):
    r = redis.Redis()
    id_artwork = cur.execute(conn, 'select count(*) from artwork').fetchall()[0][0] - 1
    query = f'''delete from artwork
                where id_artwork = {id_artwork}
                returning id_artwork;'''
    t1 = time()
    cur.execute(conn, query)
    t2 = time()
    conn.commit()

    t3 = time()
    r.delete(CACHE_KEY)
    t4 = time()
    r.close()
    return t2 - t1, t4 - t3

def update_analis(cur, conn):
    r = redis.Redis()

    # Получаем случайную запись для обновления
    cur.execute("""
        SELECT id, goal, hours 
        FROM experiment_1 
        ORDER BY RANDOM() 
        LIMIT 1
    """)
    record = cur.fetchone()
    
    if not record:
        print("Нет записей для обновления")
        return 0, 0
        
    random_id = record[0]

    max_id_author = cur.execute(conn, 'select count(*) from author').fetchall()[0][0] - 1
    id_artwork = cur.execute(conn, 'select count(*) from artwork').fetchall()[0][0] - 1

    fake = Faker()
    query = f'''update artwork
                set (id_artwork, name, style, year_create, format, id_author) = 
                    ({id_artwork}, '{fake.word()}', '{fake.word()}', 
                    '{fake.year()}', '{fake.word}', '{random.randint(0, max_id_author)}')
                where id_artwork = {id_artwork}'''

    t1 = time()
    cur.execute(conn, query)
    conn.commit()  
    t2 = time()

    cur.execute(QUERY)
    results = cur.fetchall()
    print_top(results)
    
    t3 = time()
    r.set(CACHE_KEY, json.dumps(results, default=str))
    t4 = time()
    r.close()
    
    # print(f"Обновлена запись: ID={random_id}, новая цель='{new_goal}', новый статус='{new_status}', новый эксперимент='{new_experiment}', новые часы={new_hours}")
    
    return t2 - t1, t4 - t3

def analis_time(cur, conn):
    iterations = 10  # Количество итераций для каждого теста
    interval = 10    # Интервал между операциями (10 секунд)
    
    # Массивы для хранения времени выполнения
    times_no_changes = {'db': [], 'redis': []}
    times_insert = {'db': [], 'redis': []}
    times_delete = {'db': [], 'redis': []}
    times_update = {'db': [], 'redis': []}
    x_points = np.array([i * interval for i in range(iterations)])
    print("\nНачало анализа производительности...")
    
    print("\n1. Тестирование без изменений данных...")
    for i in range(iterations):
        print(i)
        db_time, redis_time = select_analis(cur)
        times_no_changes['db'].append(db_time)
        times_no_changes['redis'].append(redis_time)
        sleep(interval)
    
    print("\n2. Тестирование с добавлением данных...")
    for i in range(iterations):
        db_time, redis_time = insert_analis(cur, conn)
        times_insert['db'].append(db_time)
        times_insert['redis'].append(redis_time)
        conn.commit()
        sleep(interval)
    
    print("\n3. Тестирование с удалением данных...")
    for i in range(iterations):
        db_time, redis_time = delete_analis(cur, conn)
        times_delete['db'].append(db_time)
        times_delete['redis'].append(redis_time)
        conn.commit()
        sleep(interval)
    
    print("\n4. Тестирование с обновлением данных...")
    for i in range(iterations):
        db_time, redis_time = update_analis(cur, conn)
        times_update['db'].append(db_time)
        times_update['redis'].append(redis_time)
        conn.commit()
        sleep(interval)
    
    # Построение графиков
    plt.figure(figsize=(15, 10))
    
    # График 1: Без изменений
    plt.subplot(2, 2, 1)
    plt.plot(x_points, times_no_changes['db'], label='PostgreSQL')
    plt.plot(x_points, times_no_changes['redis'], label='Redis')
    plt.title('Время выполнения без изменений')
    plt.legend()
    
    # График 2: Вставка
    plt.subplot(2, 2, 2)
    plt.plot(x_points, times_insert['db'], label='PostgreSQL')
    plt.plot(x_points, times_insert['redis'], label='Redis')
    plt.title('Время выполнения при вставке')
    plt.legend()
    
    # График 3: Удаление
    plt.subplot(2, 2, 3)
    plt.plot(x_points, times_delete['db'], label='PostgreSQL')
    plt.plot(x_points, times_delete['redis'], label='Redis')
    plt.title('Время выполнения при удалении')
    plt.legend()
    
    # График 4: Обновление
    plt.subplot(2, 2, 4)
    plt.plot(x_points, times_update['db'], label='PostgreSQL')
    plt.plot(x_points, times_update['redis'], label='Redis')
    plt.title('Время выполнения при обновлении')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('performance_analysis.png')
    plt.close()
    
    # print("\nАнализ завершен. Графики сохранены в файл 'performance_analysis.png'")
    
def main():
    conn = dbconnect()
    cur = conn.cursor()

    print("""
    1. Запрос на получение 10 самых долгих экспериментов
    2. Запрос на стороне БД
    3. Запрос на стороне Redis
    4. Провести сравнительный анализ времени выполнения запросов
    0. Выйти
    """)

    while True:
        choice = int(input("Выберите действие: "))
        if choice == 0:
            break
        elif choice == 1:
            data = get_top_authors(cur)
            print_top(data)
        elif choice == 2:
            print("Ctrl+C для выода в главное меню")
            while True:
                try:
                    data = get_experiments_from_db(cur)
                    print_top(data)
                    sleep(5)
                except KeyboardInterrupt:
                    print("\nВыход в главное меню")
                    break
        elif choice == 3:
            print("Ctrl+C для выхода в главное меню")
            while True:
                try:
                    data = get_experiments_from_redis(cur)
                    print_top(data)
                    sleep(5)
                except KeyboardInterrupt:
                    print("\nВыход в главное меню")
                    break
        elif choice == 4:
            analis_time(cur, conn)
        else:
            print("Ошибка! Выбрана неверная команда")
    conn.close()

if __name__ == '__main__':
    # conn = dbconnect()
    # cur = conn.cursor()
    # data = get_top_authors(cur)
    # print_top(data)
    main()
