"""
Главный модуль приложения
"""
from db.db import test_connection
from db.crud import (
    get_all_categories, 
    get_all_books, 
    get_books_by_category,
    search_books
)

def print_header(title):
    """Выводит красивый заголовок"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def print_category(category):
    """Выводит информацию о категории"""
    print(f" [{category['id']}] {category['title']}")

def print_book(book):
    """Выводит информацию о книге"""
    category = book.get('category_title', 'Без категории')
    print(f" [{book['id']}] {book['title']}")
    print(f"   Описание: {book['description'][:50]}...")
    print(f"   Цена: {book['price']} руб.")
    print(f"   Категория: {category}")
    if book.get('url'):
        print(f"   URL: {book['url']}")
    print()

def main():
    """Главная функция приложения"""
    
    print_header("КНИЖНЫЙ МАГАЗИН - ПРОСМОТР ДАННЫХ")
    
    print("\n Проверка подключения к базе данных...")
    if not test_connection():
        print(" Ошибка подключения к БД. Запустите сначала init_db.py")
        return
    
    print_header("СПИСОК КАТЕГОРИЙ")
    categories = get_all_categories()
    
    if categories:
        for category in categories:
            print_category(category)
            
            books_in_category = get_books_by_category(category['id'])
            if books_in_category:
                for book in books_in_category[:2]:  
                    print(f"   {book['title']} - {book['price']} руб.")
            else:
                print("   Нет книг в этой категории")
            print()
    else:
        print(" Категории не найдены. Запустите init_db.py для заполнения БД")
    
    print_header("ВСЕ КНИГИ")
    books = get_all_books()
    
    if books:
        print(f"Всего книг: {len(books)}\n")
        
        books_by_cat = {}
        for book in books:
            cat_title = book.get('category_title', 'Без категории')
            if cat_title not in books_by_cat:
                books_by_cat[cat_title] = []
            books_by_cat[cat_title].append(book)
        
        for category, cat_books in books_by_cat.items():
            print(f" {category}:")
            for book in cat_books:
                print(f"    {book['title']} - {book['price']} руб.")
            print()
    else:
        print(" Книги не найдены. Запустите init_db.py для заполнения БД")
    
    print_header("ПОИСК КНИГ")
    search_term = "python"
    print(f"Поиск книг по запросу '{search_term}':")
    
    found_books = search_books(search_term)
    if found_books:
        for book in found_books:
            print(f"    {book['title']} - {book['price']} руб. ({book.get('category_title', 'Без категории')})")
    else:
        print(f"   Книги по запросу '{search_term}' не найдены")
    
    print("\n" + "=" * 70)
    print(" ПРОСМОТР ДАННЫХ ЗАВЕРШЕН")
    print("=" * 70)

if __name__ == "__main__":
    main()
