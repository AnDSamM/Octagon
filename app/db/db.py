from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    echo=False  
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    """Функция для получения сессии БД (для зависимостей FastAPI)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_session():
    """Контекстный менеджер для работы с сессией"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def test_connection():
    """Тестирует подключение к базе данных"""
    try:
        with engine.connect() as conn:
            
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()  
            print("Подключение к БД успешно установлено")
            print(f"Версия PostgreSQL: {version}")
            return True
    except Exception as e:
        print(f"Ошибка при тестировании подключения: {e}")
        return False

def create_database():
    """Создает базу данных, если она не существует"""
    
    temp_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
    temp_engine = create_engine(temp_url)
    
    try:
        with temp_engine.connect() as conn:
            conn = conn.execution_options(isolation_level="AUTOCOMMIT")
            
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"), 
                {"dbname": DB_NAME}
            )
            exists = result.scalar()
            
            if not exists:
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                print(f"База данных {DB_NAME} создана")
            else:
                print(f"База данных {DB_NAME} уже существует")
            return True
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
        return False
    finally:
        temp_engine.dispose()