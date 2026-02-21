from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.db import Base, engine

class Category(Base):
    """Модель категории книг"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
    books = relationship("Book", back_populates="category", cascade="save-update")
    
    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.title}')>"

class Book(Base):
    """Модель книги"""
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    url = Column(String(500), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
    category = relationship("Category", back_populates="books")
    
    __table_args__ = (
        Index("idx_books_category", "category_id"),
    )
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', price={self.price})>"

def create_tables():
    """Создает все таблицы в базе данных"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы")
        return True
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        return False

def drop_tables():
    """Удаляет все таблицы (для очистки)"""
    try:
        Base.metadata.drop_all(bind=engine)
        print("Таблицы успешно удалены")
        return True
    except Exception as e:
        print(f"Ошибка при удалении таблиц: {e}")
        return False