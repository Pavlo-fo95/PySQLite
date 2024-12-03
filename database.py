from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Указываем путь к базе данных SQLite
DATABASE_URL = "sqlite:///./notes.db"

# Создаём движок базы данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаём сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()