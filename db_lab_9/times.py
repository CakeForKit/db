import time
import matplotlib
import matplotlib.pyplot as plt
from actions import *

N = 10
SLEEP_TIME = 2
STEP = 3
DIR = './db/db_lab_9/img'

def select(connection):
    start = time.time()
    get_top_authors(connection)
    return time.time() - start


def select_cached(connection, r):
    start = time.time()
    get_top_authors_cache(connection, r)
    return time.time() - start

def insert(connection, r):
    start = time.time()
    add_artwork(connection, r)
    return time.time() - start

def delete(connection, r):
    start = time.time()
    delete_artwork(connection, r)
    return time.time() - start

def times_select(connection, r):
    cached_time, not_cached_time = [], []

    for i in range(N):
        not_cached_time.append(select(connection))

    for i in range(N):
        cached_time.append(select_cached(connection, r))

    plt.plot(range(len(cached_time)), cached_time, label="Select с кешированием")
    plt.plot(range(len(not_cached_time)), not_cached_time, label="Select без кеширования")
    plt.legend()
    plt.savefig(f'{DIR}/select.png')
    print('saved')
    plt.show()


def times_insert(connection, r):
    cached_time, not_cached_time = [], []

    for i in range(N):
        not_cached_time.append(select(connection))
        cached_time.append(select_cached(connection, r))

        time.sleep(SLEEP_TIME)

        insert(connection, r)
        not_cached_time.append(select(connection))
        cached_time.append(select_cached(connection, r))

        time.sleep(SLEEP_TIME)

    plt.plot(range(len(cached_time)), cached_time, label="Insert + select с кешированием")
    plt.plot(range(len(not_cached_time)), not_cached_time, label="Insert + select без кеширования")
    plt.legend()
    plt.savefig(f'{DIR}/insert-select.png')

    plt.clf()


def times_delete(connection, r):
    cached_time, not_cached_time = [], []

    for i in range(N):
        not_cached_time.append(select(connection))
        cached_time.append(select_cached(connection, r))

        time.sleep(SLEEP_TIME)

        delete(connection, r)
        not_cached_time.append(select(connection))
        cached_time.append(select_cached(connection, r))

        time.sleep(SLEEP_TIME)

    plt.plot(range(len(cached_time)), cached_time, label="delete + select с кешированием")
    plt.plot(range(len(not_cached_time)), not_cached_time, label="delete + select без кеширования")
    plt.legend()
    plt.savefig(f'{DIR}/delete-select.png')

    plt.clf()



    # iterations = 10  # Количество итераций для каждого теста
    # interval = 10    # Интервал между операциями (10 секунд)
    
    # # Массивы для хранения времени выполнения
    # times_no_changes = {'db': [], 'redis': []}
    # times_insert = {'db': [], 'redis': []}
    # times_delete = {'db': [], 'redis': []}
    # times_update = {'db': [], 'redis': []}
    # x_points = np.array([i * interval for i in range(iterations)])
    # print("\nНачало анализа производительности...")
    
    # print("\n1. Тестирование без изменений данных...")
    # for i in range(iterations):
    #     print(i)
    #     db_time, redis_time = select_analis(cur)
    #     times_no_changes['db'].append(db_time)
    #     times_no_changes['redis'].append(redis_time)
    #     sleep(interval)
    
    # print("\n2. Тестирование с добавлением данных...")
    # for i in range(iterations):
    #     db_time, redis_time = insert_analis(cur, conn)
    #     times_insert['db'].append(db_time)
    #     times_insert['redis'].append(redis_time)
    #     conn.commit()
    #     sleep(interval)
    
    # print("\n3. Тестирование с удалением данных...")
    # for i in range(iterations):
    #     db_time, redis_time = delete_analis(cur, conn)
    #     times_delete['db'].append(db_time)
    #     times_delete['redis'].append(redis_time)
    #     conn.commit()
    #     sleep(interval)
    
    # print("\n4. Тестирование с обновлением данных...")
    # for i in range(iterations):
    #     db_time, redis_time = update_analis(cur, conn)
    #     times_update['db'].append(db_time)
    #     times_update['redis'].append(redis_time)
    #     conn.commit()
    #     sleep(interval)
    
    # # Построение графиков
    # plt.figure(figsize=(15, 10))
    
    # # График 1: Без изменений
    # plt.subplot(2, 2, 1)
    # plt.plot(x_points, times_no_changes['db'], label='PostgreSQL')
    # plt.plot(x_points, times_no_changes['redis'], label='Redis')
    # plt.title('Время выполнения без изменений')
    # plt.legend()
    
    # # График 2: Вставка
    # plt.subplot(2, 2, 2)
    # plt.plot(x_points, times_insert['db'], label='PostgreSQL')
    # plt.plot(x_points, times_insert['redis'], label='Redis')
    # plt.title('Время выполнения при вставке')
    # plt.legend()
    
    # # График 3: Удаление
    # plt.subplot(2, 2, 3)
    # plt.plot(x_points, times_delete['db'], label='PostgreSQL')
    # plt.plot(x_points, times_delete['redis'], label='Redis')
    # plt.title('Время выполнения при удалении')
    # plt.legend()
    
    # График 4: Обновление
    plt.subplot(2, 2, 4)
    plt.plot(x_points, times_update['db'], label='PostgreSQL')
    plt.plot(x_points, times_update['redis'], label='Redis')
    plt.title('Время выполнения при обновлении')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('performance_analysis.png')
    plt.close()