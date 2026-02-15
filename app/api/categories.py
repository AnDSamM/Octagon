from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

# Импортируем наши модули - используем полный путь от корня проекта
from app.db.crud import (
    get_all_categories,
    get_category,
    create_category,
    update_category,
    delete_category
)
from app.db.db import get_db
from app.schemas import CategoryResponse, CategoryCreate, CategoryUpdate

# Создаем роутер для категорий
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Категория не найдена"}}
)

@router.get("/", response_model=List[CategoryResponse])
async def read_categories(db=Depends(get_db)):
    """
    Получить список всех категорий
    """
    categories = get_all_categories()
    if categories is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении списка категорий"
        )
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
async def read_category(category_id: int, db=Depends(get_db)):
    """
    Получить категорию по ID
    """
    category = get_category(category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_new_category(category: CategoryCreate, db=Depends(get_db)):
    """
    Создать новую категорию
    
    - **title**: Название категории (обязательно)
    """
    # Проверяем, что название не пустое
    if not category.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Название категории не может быть пустым"
        )
    
    new_category = create_category(category.title)
    if new_category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким названием уже существует"
        )
    return new_category

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_existing_category(
    category_id: int, 
    category: CategoryUpdate, 
    db=Depends(get_db)
):
    """
    Обновить существующую категорию
    
    - **title**: Новое название категории
    """
    # Проверяем, что передано название для обновления
    if category.title is None or not category.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Название категории не может быть пустым"
        )
    
    updated_category = update_category(category_id, category.title)
    if updated_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return updated_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_category(category_id: int, db=Depends(get_db)):
    """
    Удалить категорию
    
    Внимание: При удалении категории, у книг в этой категории
    поле category_id станет NULL
    """
    deleted = delete_category(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return None  # Возвращаем None для статуса 204 No Content

# Дополнительный эндпоинт для проверки существования категории
@router.head("/{category_id}")
async def check_category_exists(category_id: int, db=Depends(get_db)):
    """
    Проверить существование категории (HEAD запрос)
    """
    category = get_category(category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return {}