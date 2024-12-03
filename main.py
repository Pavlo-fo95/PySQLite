from fastapi import FastAPI
from routes import router
from database import engine
from models import Base

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

# Создание приложения
app = FastAPI()

# Подключение маршрутов
app.include_router(router)