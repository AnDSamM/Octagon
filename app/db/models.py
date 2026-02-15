from psycopg2 import sql
from app.db.db import get_connection

def create_tables():
    """Создает все таблицы в базе данных"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                url VARCHAR(500),
                category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_books_category 
            ON books(category_id)
        """)
        
        conn.commit()
        print("Таблицы успешно созданы")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при создании таблиц: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def drop_tables():
    """Удаляет все таблицы (для очистки)"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        cur.execute("DROP TABLE IF EXISTS books CASCADE")
        cur.execute("DROP TABLE IF EXISTS categories CASCADE")
        
        conn.commit()
        print("Таблицы успешно удалены")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при удалении таблиц: {e}")
        return False
    finally:
        cur.close()
        conn.close()
