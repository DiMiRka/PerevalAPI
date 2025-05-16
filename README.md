# PerevalAPI  

Сервис для учета горных перевалов с возможностью CRUD-операций, хранения данных о перевалах, их координатах, изображениях и уровне сложности в разное время года.  

## 📌 Возможности
- Добавление новых перевалов с координатами и изображениями (`POST /pass/pass_post`)
- Получение данных о перевале по ID (`GET /pass/pass_get/`)
- Обновление данных перевала (только для статуса "new") (`PATCH /pass/pass_patch/`)
- Получение всех перевалов пользователя по email (`GET /pass/pass_get_email/`)

## 🛠️ Технологии
- **Backend**: Python 3.11, FastAPI (асинхронный)
- **База данных**: PostgreSQL, SQLAlchemy 2.0 (async)
- **Миграции**: Alembic
- **Валидация**: Pydantic v2
- **Деплой**: Docker, Docker Compose 

## Структура проекта
```
PerevalAPI/
├──alembic/                    # Миграции базы данных
│   ├── versions/              # Файлы миграций
│   ├── env.py                 # Конфигурация Alembic
│   └── script.py.mako         # Шаблон для генерации миграций
│
├── src/                       # Основной код приложения
│   │
│   ├── api/                   # API эндопоинты
│   │   └── v1/                # Версия API
│   │       ├── __init__.py
│   │       ├── pass_point.py  # Эндопоинты перевала
│   │       └── user.py        # Эндопоинты юзера
│   │
│   ├── core/		       # Конфигурационные файлы
│   │   ├── __init.py__
│   │   ├── config.py	       # Конфигурцаии сервиса
│   │   └── db_config.py       # Конфигурцаии базы данных
│   │
│   ├── models/		       # Модели данных Sqlalchemy
│   │   ├── __init.py__
│   │   ├── base.py	       # Базовая модель
│   │   ├── pass_point.py      # Модели перевала
│   │   └── user.py	       # Модель юзера
│   │
│   ├── schemas/	       # Схемы Pydantic
│   │   ├── __init.py__
│   │   ├── pass_points.py     # Схемы первала
│   │   └── users.py	       # Схемы юзера
│   │
│   ├── services/	       # Бизнес логика
│   │   ├── __init.py__
│   │   ├── pass_points.py     # Логика перевала
│   │   └── users.py	       # Логика юзера
│   │
│   └── main.py 	       # Точка входа в приложение
│
├── tests/		       # Тестирование Pytest 
│   ├── __init.py__
│   ├── conftest.py	       # Фикстуры
│   └── test_db.py	       # Тестирование операция с базой данных
│
├── .dockerignor               # Игнорируемые файлы Dcker
├── .env                       # Файл локального кружения
├── .env.docker                # Файл docker окружения
├── .gitignore                 # Игнорируемые файлы Git
├── alembic.ini                # Конфигурация Alembic
├── docker-compose.yml         # Docker конфигурация
├── Dockerfile                 # Сборка образа FastApi
├── pytest.ini		       # Конфигупация Pytest
└── requirements.txt           # Список зависимостей
```

## 🚀 Запуск проекта

### Локальный запуск
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/DiMiRka/PerevalAPI.git
   cd PerevalAPI
   ```
2. Создайте и активируйте виртуальное окружение (рекомендуется):
    ```bash
    python -m venv venv
    source venv/bin/activate  # для Linux/MacOS
    venv\Scripts\activate     # для Windows
   ```
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
   ```
4. Примените миграции:
   ```bash
   alembic upgrade head
   ```
5. Запустите сервис:
    ```bash
    python src/main.py
   ```
### Запуск через Docker
   ```bash
   docker-compose up --build -d
   ```
#### Система автоматически:
- 🐳 Создаст и запустит контейнеры
- 🔄 Применит все миграции
- 🚀 Запустит FastAPI сервер с авторелоадом

## 📄 Документация API
