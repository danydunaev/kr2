```markdown
# FastAPI Practice Project

Учебный проект для изучения FastAPI, включающий работу с Pydantic моделями, аутентификацией, cookie и заголовками HTTP.

## Содержание
- [Требования](#требования)
- [Установка](#установка)
- [Запуск](#запуск)
- [Структура проекта](#структура-проекта)
- [Задания](#задания)
  - [Задание 3.1 - Создание пользователя](#задание-31---создание-пользователя)
  - [Задание 3.2 - Работа с продуктами](#задание-32---работа-с-продуктами)
  - [Задание 5.1-5.3 - Аутентификация](#задание-51-53---аутентификация)
  - [Задание 5.4 - Заголовки запроса (raw)](#задание-54---заголовки-запроса-raw)
  - [Задание 5.5 - Заголовки с Pydantic](#задание-55---заголовки-с-pydantic)
- [Тестирование](#тестирование)
- [Примеры запросов](#примеры-запросов)

## Требования

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- itsdangerous
- email-validator

##  Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd fastapi-practice
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install fastapi uvicorn pydantic itsdangerous email-validator
```

##  Запуск

```bash
uvicorn app:app --reload --port 8000
```

После запуска откройте:
- Документация Swagger: http://127.0.0.1:8000/docs
- Альтернативная документация: http://127.0.0.1:8000/redoc

##  Структура проекта

```
├── app.py              # Основное приложение FastAPI
├── models.py           # Pydantic модели
├── README.md          # Документация
└── cookies.txt        # Файл для хранения cookie (создается автоматически)
```

##  Задания

### Задание 3.1 - Создание пользователя

**Эндпоинт:** `POST /create_user`

Создает нового пользователя с валидацией данных.

**Модель UserCreate:**
| Поле | Тип | Обязательное | Валидация |
|------|-----|--------------|-----------|
| name | str | Да | - |
| email | EmailStr | Да | Формат email |
| age | Optional[int] | Нет | > 0 |
| is_subscribed | Optional[bool] | Нет | - |

**Пример запроса:**
```json
{
  "name": "Alice",
  "email": "alice@example.com",
  "age": 30,
  "is_subscribed": true
}
```

### Задание 3.2 - Работа с продуктами

#### Получение продукта по ID
**Эндпоинт:** `GET /product/{product_id}`

**Пример:** `GET /product/123`

**Ответ:**
```json
{
  "product_id": 123,
  "name": "Smartphone",
  "category": "Electronics",
  "price": 599.99
}
```

#### Поиск продуктов
**Эндпоинт:** `GET /products/search`

**Параметры:**
- `keyword` (обязательный) - ключевое слово для поиска
- `category` (опциональный) - фильтр по категории
- `limit` (опциональный, default=10) - лимит результатов

**Пример:** `GET /products/search?keyword=phone&category=Electronics&limit=5`

### Задание 5.1-5.3 - Аутентификация

#### Вход в систему
**Эндпоинт:** `POST /login`

Устанавливает подписанную cookie `session_token` с временем жизни 5 минут.

**Модель LoginRequest:**
```json
{
  "username": "user123",
  "password": "password123"
}
```

**Особенности:**
- Используется `URLSafeTimedSerializer` для подписи
- Cookie содержит `user_id` и `timestamp`
- Время жизни cookie: 5 минут
- HttpOnly для безопасности

#### Защищенный профиль
**Эндпоинт:** `GET /profile`

Требует валидную cookie `session_token`.

**Логика обновления сессии:**
- < 3 минут с последней активности → сессия не обновляется
- 3-5 минут → сессия обновляется (+5 минут)
- \> 5 минут → ошибка 401

### Задание 5.4 - Заголовки запроса (raw)

**Эндпоинт:** `GET /headers`

Возвращает заголовки User-Agent и Accept-Language.

**Пример ответа:**
```json
{
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
  "Accept-Language": "en-US,en;q=0.9"
}
```

### Задание 5.5 - Заголовки с Pydantic

#### Заголовки через Pydantic
**Эндпоинт:** `GET /headers_pydantic`

Использует модель `CommonHeaders` для валидации заголовков.

#### Информация с серверным временем
**Эндпоинт:** `GET /info`

Возвращает заголовки + дополнительное поле + заголовок `X-Server-Time`.

**Пример ответа:**
```json
{
  "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
  "headers": {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
  }
}
```
**Заголовки ответа:** `X-Server-Time: 2024-01-01T12:00:00`

##  Тестирование

### Через Swagger UI
1. Запустите сервер
2. Откройте http://127.0.0.1:8000/docs
3. Выберите эндпоинт
4. Нажмите "Try it out"
5. Введите данные
6. Нажмите "Execute"

### Через curl

#### 3.1 - Создание пользователя
```bash
curl -X POST http://127.0.0.1:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com","age":30,"is_subscribed":true}'
```

#### 3.2 - Поиск продуктов
```bash
curl "http://127.0.0.1:8000/products/search?keyword=phone&category=Electronics&limit=5"
```

#### 5.1-5.3 - Аутентификация
```bash
# Логин (сохраняем cookie)
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user123","password":"password123"}' \
  -c cookies.txt

# Профиль (используем cookie)
curl http://127.0.0.1:8000/profile -b cookies.txt

# Проверка времени жизни (подождать 6 минут)
curl http://127.0.0.1:8000/profile -b cookies.txt  # Должно вернуть 401
```

#### 5.4 - Заголовки
```bash
curl http://127.0.0.1:8000/headers \
  -H "User-Agent: Mozilla/5.0" \
  -H "Accept-Language: en-US,en;q=0.9"
```

#### 5.5 - Info с заголовком
```bash
curl -i http://127.0.0.1:8000/info \
  -H "User-Agent: Mozilla/5.0" \
  -H "Accept-Language: en-US,en;q=0.9"
```

## 🔍 Проверка cookie

### В браузере (Chrome DevTools)
1. F12 → Application → Cookies
2. Найдите `session_token`

### Через curl
```bash
# Показать все заголовки ответа
curl -i -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user123","password":"password123"}'
```

## Возможные ошибки

| Код | Описание | Причина |
|-----|----------|---------|
| 200 | Успешно | - |
| 400 | Bad Request | Неверный формат запроса |
| 401 | Unauthorized | Неверные учетные данные или истекшая сессия |
| 404 | Not Found | Продукт не найден |
| 422 | Validation Error | Неверный формат данных |

##  Дополнительная информация

- **FastAPI документация:** https://fastapi.tiangolo.com/
- **Pydantic:** https://docs.pydantic.dev/
- **itsdangerous:** https://pythonhosted.org/itsdangerous/






