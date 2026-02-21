from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session  

from app.db.crud import (
    get_all_books,
    get_book,
    create_book,
    update_book,
    delete_book,
    get_books_by_category,
    get_category,
    search_books  
)
from app.db.db import get_db
from app.schemas import BookResponse, BookCreate, BookUpdate

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Книга не найдена"}}
)

@router.get("/", response_model=List[BookResponse])
async def read_books(
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    db: Session = Depends(get_db)  
):
    """
    Получить список всех книг.
    Можно фильтровать по категории через параметр category_id
    """
    try:
        if category_id is not None:
            
            category = get_category(db, category_id)  
            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Категория с ID {category_id} не найдена"
                )
            books = get_books_by_category(db, category_id)  
        else:
            books = get_all_books(db)  
        
        if books is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении списка книг"
            )
        return books
    except Exception as e:
        print(f"Ошибка в read_books: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{book_id}", response_model=BookResponse)
async def read_book(
    book_id: int, 
    db: Session = Depends(get_db)  
):
    """
    Получить книгу по ID
    """
    book = get_book(db, book_id)  
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_new_book(
    book: BookCreate, 
    db: Session = Depends(get_db)  
):
    """
    Создать новую книгу
    
    Поля:
    - **title**: Название книги (обязательно)
    - **description**: Описание книги
    - **price**: Цена (обязательно)
    - **url**: Ссылка на товар
    - **category_id**: ID категории (может быть null)
    """
   
    if not book.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Название книги не может быть пустым"
        )
    
    if book.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Цена должна быть больше 0"
        )
    
   
    if book.category_id is not None:
        category = get_category(db, book.category_id)  
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {book.category_id} не найдена"
            )
    
    new_book = create_book(
        db=db,  
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url or ''
    )
    
    if new_book is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при создании книги"
        )
    return new_book

@router.put("/{book_id}", response_model=BookResponse)
async def update_existing_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db)  
):
    """
    Обновить существующую книгу
    
    Можно обновлять любое из полей:
    - **title**: Новое название
    - **description**: Новое описание
    - **price**: Новая цена
    - **url**: Новая ссылка
    - **category_id**: Новый ID категории
    """
   
    existing_book = get_book(db, book_id) 
    if existing_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
   
    if book.title is not None and not book.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Название книги не может быть пустым"
        )
    
    if book.price is not None and book.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Цена должна быть больше 0"
        )
    
    
    if book.category_id is not None:
        category = get_category(db, book.category_id)  
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {book.category_id} не найдена"
            )
    
    
    update_data = {}
    if book.title is not None:
        update_data['title'] = book.title
    if book.description is not None:
        update_data['description'] = book.description
    if book.price is not None:
        update_data['price'] = book.price
    if book.category_id is not None:
        update_data['category_id'] = book.category_id
    if book.url is not None:
        update_data['url'] = book.url
    
    updated_book = update_book(
        db=db,  
        book_id=book_id,
        **update_data
    )
    
    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении книги"
        )
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_book(
    book_id: int, 
    db: Session = Depends(get_db)  
):
    """
    Удалить книгу
    """
    existing_book = get_book(db, book_id) 
    if existing_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
    deleted = delete_book(db, book_id)  
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении книги"
        )
    return None

@router.get("/search/", response_model=List[BookResponse])
async def search_books_endpoint(
    q: str = Query(..., min_length=2, description="Поисковый запрос"),
    db: Session = Depends(get_db)  
):
    """
    Поиск книг по названию или описанию
    """
    books = search_books(db, q)  
    if books is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при поиске книг"
        )
    return books