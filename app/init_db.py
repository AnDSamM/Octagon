"""
Модуль для инициализации базы данных начальными данными
"""
from db.db import create_database, test_connection
from db.models import create_tables, drop_tables
from db.crud import create_category, create_book, get_all_categories, get_all_books

def init_database():
    """Инициализирует базу данных и заполняет её тестовыми данными"""
    
    print("=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ КНИЖНОГО МАГАЗИНА")
    print("=" * 60)
    
    print("\n Шаг 1: Создание базы данных...")
    if create_database():
        print("    База данных готова")
    else:
        print("    Ошибка создания базы данных")
        return False
    
    print("\n Шаг 2: Проверка подключения...")
    if test_connection():
        print("    Подключение установлено")
    else:
        print("    Ошибка подключения")
        return False
    
    print("\n Шаг 3: Создание таблиц...")
    if create_tables():
        print("    Таблицы созданы")
    else:
        print("    Ошибка создания таблиц")
        return False
    
    print("\n Шаг 4: Добавление категорий...")
    
    categories = [
        "Программирование",
        "Базы данных", 
        "Веб-разработка",
        "Data Science"
    ]
    
    category_ids = {}
    for cat_title in categories:
        category = create_category(cat_title)
        if category:
            category_ids[cat_title] = category['id']
            print(f"    Добавлена категория: {cat_title} (ID: {category['id']})")
        else:
            print(f"    Ошибка добавления категории: {cat_title}")
    
    print("\n Шаг 5: Добавление книг...")
    
    programming_books = [
        ("Python. К вершинам мастерства", "Глубокое погружение в Python", 2499.99),
        ("Изучаем Python", "Программирование игр, визуализация данных, веб-приложения", 1999.99),
        ("Чистый код", "Создание, анализ и рефакторинг", 1799.99),
        ("Алгоритмы на Python", "Разработка и реализация", 2899.99)
    ]
    
    print("\n    Категория: Программирование")
    for title, desc, price in programming_books:
        book = create_book(title, desc, price, category_ids["Программирование"])
        if book:
            print(f"    {title} - {price} руб.")
    
    db_books = [
        ("PostgreSQL. Основы", "Работа с базами данных", 1599.99),
        ("SQL. Сборник рецептов", "Решение практических задач", 1899.99),
        ("Высоконагруженные приложения", "Масштабирование баз данных", 3299.99)
    ]
    
    print("\n  Категория: Базы данных")
    for title, desc, price in db_books:
        book = create_book(title, desc, price, category_ids["Базы данных"])
        if book:
            print(f"  {title} - {price} руб.")
    
    web_books = [
        ("Django для начинающих", "Создание веб-сайтов на Python", 2199.99),
        ("HTML и CSS", "Дизайн и разработка веб-сайтов", 1299.99),
        ("JavaScript. Подробное руководство", "Клиентская разработка", 2799.99),
        ("FastAPI. Современный веб-фреймворк", "Асинхронная разработка", 2399.99)
    ]
    
    print("\n  Категория: Веб-разработка")
    for title, desc, price in web_books:
        book = create_book(title, desc, price, category_ids["Веб-разработка"])
        if book:
            print(f"      {title} - {price} руб.")
    
    ds_books = [
        ("Python для анализа данных", "Обработка данных с pandas", 2599.99),
        ("Глубокое обучение", "Теория и практика", 3999.99),
        ("Статистика для Data Science", "Базовый курс", 1899.99)
    ]
    
    print("\nКатегория: Data Science")
    for title, desc, price in ds_books:
        book = create_book(title, desc, price, category_ids["Data Science"])
        if book:
            print(f"       {title} - {price} руб.")
    
    print("\n" + "=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
    print("=" * 60)
    
    print(f"\n Статистика:")
    categories_count = len(get_all_categories())
    books_count = len(get_all_books())
    print(f"   - Категорий: {categories_count}")
    print(f"   - Книг: {books_count}")
    
    return True

def reset_database():
    """Полностью сбрасывает базу данных"""
    print("\n Сброс базы данных...")
    if drop_tables():
        print("Таблицы удалены")
    init_database()

if __name__ == "__main__":
    init_database()
