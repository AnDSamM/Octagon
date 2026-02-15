import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os


DB_NAME = "octagon_db"
DB_USER = "octagon"
DB_PASSWORD = "12345"  
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    """Создает и возвращает подключение к базе данных"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            cursor_factory=RealDictCursor
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def create_database():
    """Создает базу данных, если она не существует"""
    try:
        
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_NAME)
            ))
            print(f"База данных {DB_NAME} создана")
        else:
            print(f"База данных {DB_NAME} уже существует")
        
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
        return False

def test_connection():
    """Тестирует подключение к базе данных"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print("Подключение к БД успешно установлено")
            print(f"Версия PostgreSQL: {version['version']}")
            cur.close()
            conn.close()
            return True
        except psycopg2.Error as e:
            print(f"Ошибка при тестировании подключения: {e}")
            return False
    return False
