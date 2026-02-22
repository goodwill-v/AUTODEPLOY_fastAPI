# Подготовка сервера Humble для автоматического деплоя FastAPI

Инструкция для коллеги: что нужно настроить на VPS перед тем, как CI/CD начнёт автоматически обновлять приложение.

---

## 1. Подготовка системы

### 1.1 Обновление и очистка диска

```bash
# Обновить пакеты
apt update && apt upgrade -y

# Очистить кеш пакетов
apt clean
apt autoclean
apt autoremove -y

# Удалить старые логи
journalctl --vacuum-time=3d

# Проверить место на диске
df -h
```

### 1.2 Удаление лишних файлов и папок

```bash
# Просмотреть использование диска по каталогам
du -sh /* 2>/dev/null | sort -rh | head -20

# Удалить неиспользуемые Docker-ресурсы (после установки Docker)
docker system prune -af --volumes   # Осторожно: удалит неиспользуемые образы, контейнеры, volumes
# Либо по отдельности:
docker image prune -af
docker container prune -f
docker volume prune -f
```

---

## 2. Удаление прежней конфигурации

### 2.1 Самоподписный SSL-сертификат

Если ранее использовался самоподписный сертификат (nginx, certbot и т.п.):

```bash
# Отключить и удалить конфигурацию nginx (если был)
systemctl stop nginx 2>/dev/null
systemctl disable nginx 2>/dev/null
apt remove --purge nginx -y 2>/dev/null

# Удалить конфиги SSL
rm -rf /etc/letsencrypt 2>/dev/null
rm -rf /etc/ssl/certs/self-signed* 2>/dev/null

# Если nginx оставляете — удалите блоки server с listen 443 и ssl_*
# Редактировать: /etc/nginx/sites-available/default
```

Приложение будет доступно по порту **8000** (HTTP). Reverse-proxy и HTTPS можно настроить позже.

### 2.2 Авторизация в registry по паролю

Если Docker ранее логинился в registry по паролю:

```bash
# Просмотреть сохранённые учётки
cat ~/.docker/config.json

# Удалить старую запись для ghcr.io (если есть)
# Отредактировать вручную или:
# Удалить файл и залогиниться заново (CI сделает это автоматически при деплое)
rm -f ~/.docker/config.json
```

Дальше авторизацию при каждом деплое выполняет GitHub Actions через Personal Access Token (PAT). Сохранённый пароль на сервере не нужен.

---

## 3. Установка Docker и Docker Compose

```bash
# Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker
usermod -aG docker $USER   # если не root

# Docker Compose (плагин)
apt install docker-compose-plugin -y

# Проверка
docker --version
docker compose version
```

---

## 4. Подготовка каталога приложения

```bash
# Создать каталог
mkdir -p /opt/fastapi-app/logs
chmod 755 /opt/fastapi-app
chmod 755 /opt/fastapi-app/logs
```

Файл `docker-compose.yml` создаётся и обновляется автоматически при каждом деплое — создавать его вручную не нужно.

---

## 5. Доступ к GHCR (опционально, для ручных проверок)

Если нужно вручную залогиниться в GitHub Container Registry:

```bash
# Создать PAT на GitHub: Settings → Developer settings → Personal access tokens
# Права: read:packages

echo "YOUR_PAT" | docker login ghcr.io -u goodwill-v --password-stdin
```

Для автоматического деплоя PAT хранится в GitHub Secrets (GH_PAT), CI подставляет его при выполнении workflow.

---

## 6. Проверка после первого деплоя

После push в `main`/`master`:

```bash
# Проверить контейнеры
docker ps

# Проверить логи
docker logs fastapi-app

# Проверить доступность API
curl http://localhost:8000/health
curl http://<IP_СЕРВЕРА>:8000/
```

---

## Краткий чек-лист

- [ ] Обновить систему и очистить диск
- [ ] Удалить старые nginx/SSL конфиги и сертификаты
- [ ] Удалить сохранённую авторизацию в registry (если была)
- [ ] Установить Docker и Docker Compose
- [ ] Создать `/opt/fastapi-app` и `/opt/fastapi-app/logs`
- [ ] Убедиться, что в GitHub Secrets заданы: GH_PAT, HOST, USERNAME, SSH_KEY
