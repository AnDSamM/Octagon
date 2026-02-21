from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.models import Category, Book
from app.db.db import SessionLocal
from typing import Optional, List, Dict, Any



def create_category(db: Session, title: str) -> Optional[Category]:
    """
    Создает новую категорию
    
    Args:
        db: Сессия базы данных
        title: Название категории
    
    Returns:
        Category: Созданная категория или None в случае ошибки
    """
    try:
        category = Category(title=title)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании категории: {e}")
        return None

def get_category(db: Session, category_id: int) -> Optional[Category]:
    """
    Получает категорию по ID
    
    Args:
        db: Сессия базы данных
        category_id: ID категории
    
    Returns:
        Category: Категория или None если не найдена
    """
    return db.query(Category).filter(Category.id == category_id).first()

def get_all_categories(db: Session) -> List[Category]:
    """
    Получает все категории
    
    Args:
        db: Сессия базы данных
    
    Returns:
        List[Category]: Список всех категорий
    """
    return db.query(Category).order_by(Category.title).all()

def update_category(db: Session, category_id: int, title: str) -> Optional[Category]:
    """
    Обновляет категорию
    
    Args:
        db: Сессия базы данных
        category_id: ID категории
        title: Новое название категории
    
    Returns:
        Category: Обновленная категория или None если не найдена
    """
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            category.title = title
            db.commit()
            db.refresh(category)
        return category
    except Exception as e:
        db.rollback()
        print(f"Ошибка при обновлении категории: {e}")
        return None

def delete_category(db: Session, category_id: int) -> bool:
    """
    Удаляет категорию
    
    Args:
        db: Сессия базы данных
        category_id: ID категории
    
    Returns:
        bool: True если удаление успешно, False если категория не найдена или ошибка
    """
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            db.delete(category)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"Ошибка при удалении категории: {e}")
        return False



def create_book(
    db: Session, 
    title: str, 
    price: float, 
    description: Optional[str] = None, 
    category_id: Optional[int] = None, 
    url: str = ''
) -> Optional[Book]:
    """
    Создает новую книгу
    
    Args:
        db: Сессия базы данных
        title: Название книги
        price: Цена книги
        description: Описание книги (опционально)
        category_id: ID категории (опционально)
        url: URL на книгу (опционально)
    
    Returns:
        Book: Созданная книга или None в случае ошибки
    """
    try:
        book = Book(
            title=title,
            description=description,
            price=price,
            category_id=category_id,
            url=url
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании книги: {e}")
        return None

def get_book(db: Session, book_id: int) -> Optional[Book]:
    """
    Получает книгу по ID
    
    Args:
        db: Сессия базы данных
        book_id: ID книги
    
    Returns:
        Book: Книга или None если не найдена
    """
    return db.query(Book).filter(Book.id == book_id).first()

def get_all_books(db: Session, category_id: Optional[int] = None) -> List[Book]:
    """
    Получает все книги, опционально фильтрует по категории
    
    Args:
        db: Сессия базы данных
        category_id: ID категории для фильтрации (опционально)
    
    Returns:
        List[Book]: Список книг
    """
    query = db.query(Book)
    if category_id is not None:
        query = query.filter(Book.category_id == category_id)
    return query.order_by(Book.title).all()

def update_book(db: Session, book_id: int, **kwargs) -> Optional[Book]:
    """
    Обновляет книгу
    
    Args:
        db: Сессия базы данных
        book_id: ID книги
        **kwargs: Поля для обновления (title, description, price, category_id, url)
    
    Returns:
        Book: Обновленная книга или None если не найдена
    """
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            return None
        
        
        for key, value in kwargs.items():
            if hasattr(book, key) and value is not None:
                setattr(book, key, value)
        
        db.commit()
        db.refresh(book)
        return book
    except Exception as e:
        db.rollback()
        print(f"Ошибка при обновлении книги: {e}")
        return None

def delete_book(db: Session, book_id: int) -> bool:
    """
    Удаляет книгу
    
    Args:
        db: Сессия базы данных
        book_id: ID книги
    
    Returns:
        bool: True если удаление успешно, False если книга не найдена или ошибка
    """
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            db.delete(book)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"Ошибка при удалении книги: {e}")
        return False

def get_books_by_category(db: Session, category_id: int) -> List[Book]:
    """
    Получает все книги в определенной категории
    
    Args:
        db: Сессия базы данных
        category_id: ID категории
    
    Returns:
        List[Book]: Список книг в категории
    """
    return db.query(Book).filter(Book.category_id == category_id).order_by(Book.title).all()

def search_books(db: Session, query: str) -> List[Book]:
    """
    Поиск книг по названию или описанию
    
    Args:
        db: Сессия базы данных
        query: Поисковый запрос
    
    Returns:
        List[Book]: Список найденных книг
    """
    search = f"%{query}%"
    return db.query(Book).filter(
        or_(
            Book.title.ilike(search),
            Book.description.ilike(search)
        )
    ).order_by(Book.title).all()

def count_books(db: Session, category_id: Optional[int] = None) -> int:
    """
    Подсчитывает количество книг
    
    Args:
        db: Сессия базы данных
        category_id: ID категории для фильтрации (опционально)
    
    Returns:
        int: Количество книг
    """
    query = db.query(Book)
    if category_id is not None:
        query = query.filter(Book.category_id == category_id)
    return query.count()

def count_categories(db: Session) -> int:
    """
    Подсчитывает количество категорий
    
    Args:
        db: Сессия базы данных
    
    Returns:
        int: Количество категорий
    """
    return db.query(Category).count()



def create_category_simple(title: str) -> Optional[Category]:
    """Обертка для create_category без передачи сессии"""
    db = SessionLocal()
    try:
        return create_category(db, title)
    finally:
        db.close()

def get_category_simple(category_id: int) -> Optional[Category]:
    """Обертка для get_category без передачи сессии"""
    db = SessionLocal()
    try:
        return get_category(db, category_id)
    finally:
        db.close()

def get_all_categories_simple() -> List[Category]:
    """Обертка для get_all_categories без передачи сессии"""
    db = SessionLocal()
    try:
        return get_all_categories(db)
    finally:
        db.close()

def update_category_simple(category_id: int, title: str) -> Optional[Category]:
    """Обертка для update_category без передачи сессии"""
    db = SessionLocal()
    try:
        return update_category(db, category_id, title)
    finally:
        db.close()

def delete_category_simple(category_id: int) -> bool:
    """Обертка для delete_category без передачи сессии"""
    db = SessionLocal()
    try:
        return delete_category(db, category_id)
    finally:
        db.close()

def create_book_simple(
    title: str, 
    price: float, 
    description: Optional[str] = None, 
    category_id: Optional[int] = None, 
    url: str = ''
) -> Optional[Book]:
    """Обертка для create_book без передачи сессии"""
    db = SessionLocal()
    try:
        return create_book(db, title, price, description, category_id, url)
    finally:
        db.close()

def get_book_simple(book_id: int) -> Optional[Book]:
    """Обертка для get_book без передачи сессии"""
    db = SessionLocal()
    try:
        return get_book(db, book_id)
    finally:
        db.close()

def get_all_books_simple(category_id: Optional[int] = None) -> List[Book]:
    """Обертка для get_all_books без передачи сессии"""
    db = SessionLocal()
    try:
        return get_all_books(db, category_id)
    finally:
        db.close()

def update_book_simple(book_id: int, **kwargs) -> Optional[Book]:
    """Обертка для update_book без передачи сессии"""
    db = SessionLocal()
    try:
        return update_book(db, book_id, **kwargs)
    finally:
        db.close()

def delete_book_simple(book_id: int) -> bool:
    """Обертка для delete_book без передачи сессии"""
    db = SessionLocal()
    try:
        return delete_book(db, book_id)
    finally:
        db.close()

def get_books_by_category_simple(category_id: int) -> List[Book]:
    """Обертка для get_books_by_category без передачи сессии"""
    db = SessionLocal()
    try:
        return get_books_by_category(db, category_id)
    finally:
        db.close()

def search_books_simple(query: str) -> List[Book]:
    """Обертка для search_books без передачи сессии"""
    db = SessionLocal()
    try:
        return search_books(db, query)
    finally:
        db.close()