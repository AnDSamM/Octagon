from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class CategoryBase(BaseModel):
    title: str

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = None
    category_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class BookCreate(BookBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    category_id: Optional[int] = None

class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookResponse(BookBase):
    id: int
    category_title: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class CategoryWithBooksResponse(CategoryResponse):
    books: List[BookResponse] = []