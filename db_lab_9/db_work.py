import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_SETTINGS = {
    "name": "postgres",
    "host": "localhost",
    "user": "root",
    "password": "postgres",
    "port": 5433
}

def table_exists(con, table_str):
    exists = False
    try:
        cur = con.cursor()
        cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
        exists = cur.fetchone()[0]
    except psycopg2.Error as e:
        print(e)
    return exists


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        connection.rollback()
        return None

    return cursor


def connect():
    connection = psycopg2.connect(
        user=DB_SETTINGS['user'],
        password=DB_SETTINGS['password'],
        host=DB_SETTINGS['host'],
        port=DB_SETTINGS['port'],
        database=DB_SETTINGS['name']
    )

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


def create_database(config):
    connection = psycopg2.connect(
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = connection.cursor()

    print(f"Server version {cursor.fetchone()}")

    create_database_query = f"CREATE DATABASE {config['name']}"
    cursor.execute(create_database_query)
    print(f"table {config['name']} successfully created")

    return connection

