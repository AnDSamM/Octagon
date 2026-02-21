from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = None
    category_id: Optional[int] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    category_id: Optional[int] = None

class BookResponse(BookBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    category_title: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class CategoryWithBooksResponse(CategoryResponse):
    books: List[BookResponse] = []