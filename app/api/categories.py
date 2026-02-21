from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.db.crud import get_all_categories, get_category, create_category, update_category, delete_category
from app.db.db import get_db
from app.schemas import CategoryResponse, CategoryCreate, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Категория не найдена"}}
)

@router.get("/", response_model=List[CategoryResponse])
async def read_categories(db: Session = Depends(get_db)):
    """Получить список всех категорий"""
    categories = get_all_categories(db)
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
async def read_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    if not category.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Название категории не может быть пустым"
        )
    
    new_category = create_category(db, category.title)
    if not new_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким названием уже существует"
        )
    return new_category

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_existing_category(
    category_id: int, 
    category: CategoryUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить существующую категорию"""
    if not category.title or not category.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Название категории не может быть пустым"
        )
    
    updated_category = update_category(db, category_id, category.title)
    if not updated_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return updated_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию"""
    deleted = delete_category(db, category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return None