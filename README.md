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
- **Тестирование**: Pytest

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
4. Примените миграции alembic:
   ```bash
   alembic stamp head
   alembic revision --autogenerate -m "fix_models"
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

## ⚙ Конфигурация
Проект поддерживает два типа окружения:
### 1. Локальное окружение (.env)
Используется при запуске без Docker:
```ini
# Настройки PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=dima-784512
POSTGRES_DB=Pereval

# Настройки приложения
HOST=localhost
PORT=8000
DOCKER_MODE=0
```
### 2. Docker окружение (.env.docker)
Используется при запуске через Docker Compose:
```ini
# Настройки PostgreSQL
POSTGRES_HOST=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
POSTGRES_DB=Pereval

# Настройки приложения
HOST=0.0.0.0
PORT=8000
RELOAD=true
DOCKER_MODE=1
```
## 📄 Документация API
После запуска сервера доступны интерактивные документации:\
**Swagger UI** (интерактивное тестирование): `http://localhost:8000/api/openapi`

### Эндопоинты:
- POST /pass/pass_post:
  - **Назначение**: Отправка перевала для сохранения
  - **Пример тела запроса в формате json**
     ```json
     {
         "beauty_title": "string",
         "title": "string",
         "other_titles": "string",
         "connect": "string",
         "add_time": "2025-05-16T11:41:32.165Z",
         "user": {
            "email": "user@example.com",
            "fam": "string",
            "name": "string",
            "otc": "string",
            "phone": "string"
         },
         "coords": {
            "latitude": 0,
            "longitude": 0,
            "height": 0
         },
         "level": {
            "winter": "string",
            "summer": "string",
            "autumn": "string",
            "spring": "string"
         },
         "images": [
            {
               "data": "string",
               "title": "string"
            }
         ]
     }
     ```
  - **Ответ**: Если перевал успешно добавлен:
    ```
    "status": 200, 
    "message": "Отправлено успешно",
    "id": id созданного перевала"
    ```
- GET /pass/pass_get:
  - **Назначение**: Получение информации по перевалу 
  - **Передаём:** id перевала в запрос
  - **Ответ**: json тело с полной информацией по перевалу 
- PATCH /pass/pass_patch:
  - **Назначение:** Редактирование информации перевала при статусе "new" 
  - **Передаём:** id перевала в запрос + json перевала, исключая информацию по user
  - **Пример тела запроса в формате json**
    ```json
     {
         "beauty_title": "string",
         "title": "string",
         "other_titles": "string",
         "connect": "string",
         "add_time": "2025-05-16T11:41:32.165Z",
         "coords": {
            "latitude": 0,
            "longitude": 0,
            "height": 0
         },
         "level": {
            "winter": "string",
            "summer": "string",
            "autumn": "string",
            "spring": "string"
         },
         "images": [
            {
               "data": "string",
               "title": "string"
            }
         ]
     }
     ```
  - **Ответ**: Если перевал успешно обновлен:
    ```
    "state": 1, 
    "message": "Успешно обновлен"
    ```
- GET /pass/pass_get_email:
  - **Назначение**: Получение всех перевалов, созданных пользователем  
  - **Передаём:** email пользователся
  - **Ответ:** Список всех перевалов, созданных пользователем в формате json
