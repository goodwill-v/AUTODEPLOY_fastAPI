# FastAPI Template Application

Шаблонное FastAPI приложение с Docker и настройками для деплоя.

## Возможности

- ✅ RESTful API с CRUD операциями
- ✅ Автоматическая документация Swagger/OpenAPI
- ✅ Docker контейнеризация
- ✅ Docker Compose для удобного деплоя
- ✅ Health check endpoint
- ✅ CORS middleware
- ✅ Готовая структура для расширения

## Быстрый старт

### Локальная разработка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите приложение:
```bash
python main.py
```

Или с помощью uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Откройте в браузере:
- API: http://localhost:8000
- Документация: http://localhost:8000/docs
- Альтернативная документация: http://localhost:8000/redoc

### Docker

1. Соберите образ:
```bash
docker build -t fastapi-app .
```

2. Запустите контейнер:
```bash
docker run -p 8000:8000 fastapi-app
```

### Docker Compose

1. Запустите приложение:
```bash
docker-compose up -d
```

2. Остановите приложение:
```bash
docker-compose down
```

3. Просмотр логов:
```bash
docker-compose logs -f
```

## API Endpoints

- `GET /` - Корневой endpoint
- `GET /health` - Health check
- `GET /items` - Получить все элементы
- `GET /items/{item_id}` - Получить элемент по ID
- `POST /items` - Создать новый элемент
- `PUT /items/{item_id}` - Обновить элемент
- `DELETE /items/{item_id}` - Удалить элемент

## Примеры запросов

### Создать элемент
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тестовый товар",
    "description": "Описание товара",
    "price": 99.99,
    "tax": 10.0
  }'
```

### Получить все элементы
```bash
curl "http://localhost:8000/items"
```

### Получить элемент по ID
```bash
curl "http://localhost:8000/items/1"
```

## Деплой

### Production рекомендации

1. Измените настройки CORS в `main.py` на конкретные домены
2. Используйте переменные окружения для конфигурации
3. Настройте reverse proxy (nginx) перед приложением
4. Используйте процесс-менеджер (systemd, supervisor) или оркестратор (Kubernetes)
5. Настройте логирование и мониторинг

### Переменные окружения

Скопируйте `.env.example` в `.env` и настройте переменные:
```bash
cp .env.example .env
```

## Структура проекта

```
fastapi_app/
├── main.py              # Основное приложение
├── requirements.txt     # Python зависимости
├── Dockerfile           # Docker образ
├── docker-compose.yml   # Docker Compose конфигурация
├── .dockerignore       # Исключения для Docker
├── .env.example        # Пример переменных окружения
└── README.md           # Документация
```

## Лицензия

MIT

---

## Руководство для новичков: Как использовать API

Если вы впервые работаете с API, этот раздел поможет вам понять основы и начать использовать это приложение.

### Что такое API?

API (Application Programming Interface) — это способ общения между программами. Представьте, что API — это официант в ресторане: вы делаете заказ (отправляете запрос), а официант приносит вам блюдо (возвращает ответ).

### Шаг 1: Запустите приложение

Сначала убедитесь, что приложение запущено:

```bash
python main.py
```

Вы должны увидеть сообщение о том, что сервер запущен на `http://localhost:8000`.

### Шаг 2: Откройте интерактивную документацию

Самый простой способ начать работу — использовать встроенную документацию:

1. Откройте браузер и перейдите по адресу: **http://localhost:8000/docs**
2. Вы увидите страницу Swagger UI со всеми доступными операциями
3. Здесь вы можете:
   - Видеть все доступные endpoints (точки входа в API)
   - Пробовать выполнять запросы прямо в браузере
   - Видеть примеры данных и ответов

### Шаг 3: Попробуйте простые операции

#### Вариант 1: Использование браузера (самый простой способ)

**1. Проверка работы API:**
   - Откройте: http://localhost:8000
   - Вы увидите приветственное сообщение

**2. Проверка здоровья сервера:**
   - Откройте: http://localhost:8000/health
   - Должен вернуться ответ: `{"status": "healthy"}`

**3. Получение списка элементов:**
   - Откройте: http://localhost:8000/items
   - Пока список пуст: `[]`

#### Вариант 2: Использование Swagger UI (рекомендуется для новичков)

1. Откройте http://localhost:8000/docs
2. Найдите раздел **POST /items** и нажмите "Try it out"
3. Замените пример данных на свои:
   ```json
   {
     "name": "Мой первый товар",
     "description": "Это описание моего товара",
     "price": 150.50,
     "tax": 15.0
   }
   ```
4. Нажмите "Execute"
5. Вы увидите ответ с созданным элементом и его ID

**Теперь попробуйте получить созданный элемент:**
1. Найдите раздел **GET /items/{item_id}**
2. Нажмите "Try it out"
3. Введите ID (обычно это `1` для первого элемента)
4. Нажмите "Execute"
5. Вы увидите данные вашего товара

#### Вариант 3: Использование curl (для командной строки)

**Создать новый элемент:**
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ноутбук",
    "description": "Игровой ноутбук",
    "price": 75000,
    "tax": 7500
  }'
```

**Получить все элементы:**
```bash
curl http://localhost:8000/items
```

**Получить элемент по ID (например, ID=1):**
```bash
curl http://localhost:8000/items/1
```

**Обновить элемент:**
```bash
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Обновленный ноутбук",
    "description": "Новое описание",
    "price": 80000,
    "tax": 8000
  }'
```

**Удалить элемент:**
```bash
curl -X DELETE "http://localhost:8000/items/1"
```

#### Вариант 4: Использование Python

Создайте файл `test_api.py`:

```python
import requests

# Базовый URL API
BASE_URL = "http://localhost:8000"

# 1. Проверка работы API
response = requests.get(f"{BASE_URL}/")
print("Приветствие:", response.json())

# 2. Создание нового элемента
new_item = {
    "name": "Смартфон",
    "description": "Флагманский смартфон",
    "price": 50000,
    "tax": 5000
}
response = requests.post(f"{BASE_URL}/items", json=new_item)
created_item = response.json()
print("Создан элемент:", created_item)
item_id = created_item["id"]

# 3. Получение всех элементов
response = requests.get(f"{BASE_URL}/items")
all_items = response.json()
print("Все элементы:", all_items)

# 4. Получение элемента по ID
response = requests.get(f"{BASE_URL}/items/{item_id}")
item = response.json()
print("Элемент по ID:", item)

# 5. Обновление элемента
updated_item = {
    "name": "Обновленный смартфон",
    "description": "Новое описание",
    "price": 55000,
    "tax": 5500
}
response = requests.put(f"{BASE_URL}/items/{item_id}", json=updated_item)
print("Обновленный элемент:", response.json())

# 6. Удаление элемента
response = requests.delete(f"{BASE_URL}/items/{item_id}")
print("Элемент удален, статус:", response.status_code)
```

Запустите скрипт:
```bash
pip install requests
python test_api.py
```

#### Вариант 5: Использование JavaScript (для веб-разработчиков)

```javascript
const BASE_URL = 'http://localhost:8000';

// 1. Создание элемента
async function createItem() {
  const response = await fetch(`${BASE_URL}/items`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: 'Планшет',
      description: 'Графический планшет',
      price: 25000,
      tax: 2500
    })
  });
  const data = await response.json();
  console.log('Создан элемент:', data);
  return data.id;
}

// 2. Получение всех элементов
async function getAllItems() {
  const response = await fetch(`${BASE_URL}/items`);
  const data = await response.json();
  console.log('Все элементы:', data);
  return data;
}

// 3. Получение элемента по ID
async function getItemById(id) {
  const response = await fetch(`${BASE_URL}/items/${id}`);
  const data = await response.json();
  console.log('Элемент:', data);
  return data;
}

// Использование:
createItem().then(id => {
  getAllItems();
  getItemById(id);
});
```

### Понимание HTTP методов

- **GET** — получить данные (чтение)
- **POST** — создать новые данные
- **PUT** — обновить существующие данные
- **DELETE** — удалить данные

### Понимание кодов ответов

- **200** — успешно
- **201** — успешно создано
- **404** — не найдено
- **500** — ошибка сервера

### Полезные советы

1. **Всегда начинайте с Swagger UI** (`/docs`) — это самый простой способ понять API
2. **Используйте Postman или Insomnia** — специальные программы для тестирования API
3. **Проверяйте формат данных** — API ожидает JSON формат
4. **Обрабатывайте ошибки** — всегда проверяйте код ответа перед использованием данных

### Что дальше?

После того как вы освоите базовые операции:
- Изучите документацию FastAPI: https://fastapi.tiangolo.com/
- Добавьте базу данных для хранения данных
- Добавьте аутентификацию и авторизацию
- Создайте свой собственный API с нужными вам endpoints

Удачи в изучении API! 🚀
