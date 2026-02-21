from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.categories import router as categories_router  
from app.api.books import router as books_router            
from app.db.db import test_connection
from app.db.models import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" Запуск приложения...")
    if not test_connection():
        print(" Внимание: Проблемы с подключением к базе данных")
    else:
        print(" База данных подключена")
        create_tables()
        print(" Таблицы проверены/созданы")
    yield
    print(" Приложение остановлено")

app = FastAPI(
    title="Bookstore API",
    description="API для управления книгами и категориями",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(categories_router)
app.include_router(books_router)

@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в Bookstore API",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "categories": "/categories",
            "books": "/books",
            "books/search": "/books/search?q=поиск",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    db_status = "connected" if test_connection() else "disconnected"
    return {
        "status": "healthy",
        "database": db_status,
        "api_version": "1.0.0"
    }