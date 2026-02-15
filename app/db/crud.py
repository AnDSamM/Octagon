
from psycopg2 import sql
from db.db import get_connection

# ========== CRUD для таблицы categories ==========

def create_category(title):
    """Создает новую категорию"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO categories (title) VALUES (%s) RETURNING id, title, created_at",
            (title,)
        )
        category = cur.fetchone()
        conn.commit()
        return category
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при создании категории: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_category(category_id):
    """Получает категорию по ID"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
        category = cur.fetchone()
        return category
    except Exception as e:
        print(f"Ошибка при получении категории: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_all_categories():
    """Получает все категории"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories ORDER BY title")
        categories = cur.fetchall()
        return categories
    except Exception as e:
        print(f"Ошибка при получении категорий: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def update_category(category_id, title):
    """Обновляет категорию"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE categories SET title = %s WHERE id = %s RETURNING *",
            (title, category_id)
        )
        category = cur.fetchone()
        conn.commit()
        return category
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при обновлении категории: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def delete_category(category_id):
    """Удаляет категорию"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM categories WHERE id = %s RETURNING id", (category_id,))
        deleted = cur.fetchone()
        conn.commit()
        return deleted is not None
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при удалении категории: {e}")
        return False
    finally:
        cur.close()
        conn.close()

# ========== CRUD для таблицы books ==========

def create_book(title, description, price, category_id=None, url=''):
    """Создает новую книгу"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO books (title, description, price, category_id, url) 
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING *
        """, (title, description, price, category_id, url))
        book = cur.fetchone()
        conn.commit()
        return book
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при создании книги: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_book(book_id):
    """Получает книгу по ID"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT b.*, c.title as category_title 
            FROM books b 
            LEFT JOIN categories c ON b.category_id = c.id 
            WHERE b.id = %s
        """, (book_id,))
        book = cur.fetchone()
        return book
    except Exception as e:
        print(f"Ошибка при получении книги: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_all_books(category_id=None):
    """Получает все книги, опционально фильтрует по категории"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        if category_id:
            cur.execute("""
                SELECT b.*, c.title as category_title 
                FROM books b 
                LEFT JOIN categories c ON b.category_id = c.id 
                WHERE b.category_id = %s
                ORDER BY b.title
            """, (category_id,))
        else:
            cur.execute("""
                SELECT b.*, c.title as category_title 
                FROM books b 
                LEFT JOIN categories c ON b.category_id = c.id 
                ORDER BY b.title
            """)
        books = cur.fetchall()
        return books
    except Exception as e:
        print(f"Ошибка при получении книг: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def update_book(book_id, title=None, description=None, price=None, category_id=None, url=None):
    """Обновляет книгу"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        
        # Получаем текущие данные книги
        cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        current = cur.fetchone()
        if not current:
            return None
        
        # Обновляем только переданные поля
        updates = []
        values = []
        
        if title is not None:
            updates.append("title = %s")
            values.append(title)
        if description is not None:
            updates.append("description = %s")
            values.append(description)
        if price is not None:
            updates.append("price = %s")
            values.append(price)
        if category_id is not None:
            updates.append("category_id = %s")
            values.append(category_id)
        if url is not None:
            updates.append("url = %s")
            values.append(url)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        
        values.append(book_id)
        
        query = f"UPDATE books SET {', '.join(updates)} WHERE id = %s RETURNING *"
        
        cur.execute(query, values)
        book = cur.fetchone()
        conn.commit()
        return book
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при обновлении книги: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def delete_book(book_id):
    """Удаляет книгу"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id = %s RETURNING id", (book_id,))
        deleted = cur.fetchone()
        conn.commit()
        return deleted is not None
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при удалении книги: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def get_books_by_category(category_id):
    """Получает все книги в определенной категории"""
    return get_all_books(category_id)

def search_books(query):
    """Поиск книг по названию или описанию"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT b.*, c.title as category_title 
            FROM books b 
            LEFT JOIN categories c ON b.category_id = c.id 
            WHERE b.title ILIKE %s OR b.description ILIKE %s
            ORDER BY b.title
        """, (f'%{query}%', f'%{query}%'))
        books = cur.fetchall()
        return books
    except Exception as e:
        print(f"Ошибка при поиске книг: {e}")
        return []
    finally:
        cur.close()
        conn.close()
