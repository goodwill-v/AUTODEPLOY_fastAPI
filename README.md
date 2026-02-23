# Деплой FastAPI через GitHub Container Registry

Автоматический деплой приложения на сервер: при push в репозиторий образ собирается, публикуется в GitHub Container Registry (GHCR) и разворачивается на VPS.

---

## 1. Деплой через GitHub Container Registry на сервер

### 1.1 Общая схема

1. Разработчик пушит код в ветку `main` или `master` (или запускает workflow вручную).
2. **GitHub Actions** собирает Docker-образ по `Dockerfile` и пушит его в **GHCR** (`ghcr.io/goodwill-v/autodeploy_fastapi`).
3. Тот же workflow по SSH подключается к серверу, копирует `docker-compose.prod.yml`, логинится в GHCR, подтягивает новый образ и перезапускает контейнер.

В итоге приложение доступно по адресу сервера, например: **http://147.45.245.124:8000/docs**

### 1.2 Настройка GitHub

**Репозиторий:** [goodwill-v/AUTODEPLOY_fastAPI](https://github.com/goodwill-v/AUTODEPLOY_fastAPI)

**Секреты репозитория** (Settings → Secrets and variables → Actions):

| Секрет    | Описание |
|----------|----------|
| `GH_PAT` | Personal Access Token (GitHub) с правом `read:packages` (для доступа к GHCR с сервера) |
| `HOST`   | IP или hostname VPS (например, `147.45.245.124`) |
| `USERNAME` | Пользователь SSH (например, `root`) |
| `SSH_KEY` | Приватный SSH-ключ для доступа к серверу |

**Workflow permissions:** в настройках репозитория включите доступ workflow к GitHub Container Registry (Settings → Actions → General → Workflow permissions → Read and write permissions).

### 1.3 Подготовка сервера

На VPS нужно один раз установить Docker и подготовить каталог. Подробная инструкция — в файле **[SERVER_SETUP.md](SERVER_SETUP.md)**. Кратко:

1. **Установить Docker и Docker Compose:**
   ```bash
   curl -fsSL https://get.docker.com | sh
   apt install docker-compose-plugin -y
   ```

2. **Создать каталог приложения:**
   ```bash
   mkdir -p /opt/fastapi-app/logs
   ```

3. **Ничего больше вручную не требуется:** файл `docker-compose.prod.yml` на сервер копирует workflow при каждом деплое.

После первого успешного деплоя приложение будет слушать порт **8000**. Проверка: `http://<IP_СЕРВЕРА>:8000/` и `http://<IP_СЕРВЕРА>:8000/docs`.

### 1.4 Что делает workflow при деплое

- **Job `build-and-push`:** checkout → сборка образа → push в GHCR с тегами `latest` и SHA коммита.
- **Job `deploy`:** после успешного push:
  - создаётся каталог `/opt/fastapi-app/logs` при необходимости;
  - на сервер копируется `docker-compose.prod.yml`;
  - выполняется вход в GHCR по `GH_PAT`;
  - старый контейнер останавливается и удаляется;
  - подтягивается новый образ и запускается `docker compose up -d`.

Файл workflow: [.github/workflows/deploy.yml](.github/workflows/deploy.yml).

### 1.5 Ручной запуск деплоя

В репозитории: **Actions** → **Build, Push to GHCR and Deploy** → **Run workflow** → выбрать ветку и запустить.

---

## 2. Использование Makefile

Makefile упрощает сборку и публикацию образа в GHCR и коммит в репозиторий.

### 2.1 Переменные

| Переменная | Значение по умолчанию | Описание |
|------------|------------------------|----------|
| `VERSION`  | из `git describe --tags` или `0.0.1` | Тег образа (без префикса `v`) |
| `MSG`      | `тест_Х` | Сообщение коммита для цели `commit` |

Образ: **`ghcr.io/goodwill-v/autodeploy_fastapi`**.

### 2.2 Цели

| Команда | Описание |
|---------|----------|
| `make help` | Справка по целям и переменным |
| `make login` | Вход в GHCR. Токен передаётся через stdin: `echo $GH_PAT \| make login` |
| `make build` | Сборка образа с тегами `$(VERSION)` и `latest` |
| `make push` | Сборка (если нужно) и пуш обоих тегов в GHCR |
| `make build-push` | Сначала `login`, затем сборка и пуш |
| `make commit` | `git init`, `git add .`, коммит с сообщением `commit: $(MSG)`, ветка `main`, пуш в `origin` |

### 2.3 Примеры

```bash
# Справка
make help

# Сборка с версией по умолчанию
make build

# Сборка с указанной версией
make build VERSION=1.2.0

# Публикация в GHCR (сначала залогиниться)
echo $GH_PAT | make login
make push

# Или одной командой (токен через stdin)
echo $GH_PAT | make build-push

# Коммит с сообщением по умолчанию ("commit: тест_Х")
make commit

# Коммит с своим сообщением
make commit MSG="fix: обновлен deploy"
```

Перед первым `make commit` задайте remote:
```bash
git remote add origin https://github.com/goodwill-v/AUTODEPLOY_fastAPI.git
```

---

## 3. Описание приложения FastAPI

Шаблонное FastAPI приложение с REST API, Docker и настройками для деплоя.

### Возможности

- RESTful API с CRUD по элементам (items)
- Документация Swagger/OpenAPI (`/docs`, `/redoc`)
- Docker и Docker Compose
- Health check `/health`, CORS middleware

### Локальная разработка

```bash
pip install -r requirements.txt
python main.py
# или
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000  
- Документация: http://localhost:8000/docs  

### Docker (локально)

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Приветствие |
| GET | `/health` | Health check |
| GET | `/items` | Список элементов |
| GET | `/items/{item_id}` | Элемент по ID |
| POST | `/items` | Создать элемент |
| PUT | `/items/{item_id}` | Обновить элемент |
| DELETE | `/items/{item_id}` | Удалить элемент |

### Примеры запросов

**Создать элемент:**
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "Товар", "description": "Описание", "price": 99.99, "tax": 10.0}'
```

**Получить все элементы:**
```bash
curl "http://localhost:8000/items"
```

### Структура проекта

```
fastapi_app/
├── main.py                 # Приложение FastAPI
├── requirements.txt        # Зависимости Python
├── Dockerfile              # Образ для production
├── docker-compose.yml      # Локальная разработка
├── docker-compose.prod.yml # Production (образ из GHCR)
├── .github/workflows/deploy.yml  # CI/CD: сборка, GHCR, деплой
├── Makefile                # Сборка, пуш образа, коммит
├── SERVER_SETUP.md         # Подготовка сервера к деплою
└── README.md               # Документация
```

### Рекомендации для production

- Ограничить CORS в `main.py` конкретными доменами.
- Использовать переменные окружения для конфигурации.
- При необходимости поставить перед приложением reverse proxy (nginx) и настроить HTTPS.

---

## Лицензия

MIT
