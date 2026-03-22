# Инструкции по установке и запуску проекта

## Базовый пример API Сервиса для магазина

### Системные требования

- Python 3.11+
- PostgreSQL 11+ (опционально, можно использовать SQLite для разработки)
- Redis (для Celery)
- Git

### Установка проекта

#### 1. Клонирование репозитория

```bash
git config --global user.name "YOUR_USERNAME"
git config --global user.email "your_email_address@example.com"

mkdir ~/my_diplom
cd my_diplom
git clone <repository_url>
cd netology_pd_diplom
```

#### 2. Создание виртуального окружения

```bash
# Для Windows
python -m venv venv
venv\Scripts\activate

# Для Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Установка зависимостей

```bash
# Обновление pip
python -m pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt
```

#### 4. Настройка базы данных

**Для разработки (SQLite):**
База данных SQLite уже настроена в проекте по умолчанию.

**Для production (PostgreSQL):**

```bash
# Установка PostgreSQL (Ubuntu/Debian)
sudo nano /etc/apt/sources.list.d/pgdg.list
# Добавить строку:
deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-11 postgresql-server-dev-11

# Настройка базы данных
sudo -u postgres psql postgres
CREATE USER diplom_user WITH PASSWORD 'password';
ALTER ROLE diplom_user SET client_encoding TO 'utf8';
ALTER ROLE diplom_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE diplom_user SET timezone TO 'Europe/Moscow';
CREATE DATABASE diplom_db OWNER diplom_user;
ALTER USER diplom_user CREATEDB;
\q
```

#### 5. Настройка Redis (для Celery)

```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# Запуск Redis
sudo service redis-server start

# Проверка работы
redis-cli ping
```

#### 6. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### 7. Выполнение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 8. Создание суперпользователя

```bash
python manage.py createsuperuser
```

#### 9. Проверка работы модулей

```bash
python manage.py runserver 0.0.0.0:8000
```

Откройте в браузере `http://localhost:8000/admin/` для проверки админ-панели.

### Запуск в production режиме

#### 1. Запуск Celery Worker

```bash
# В новом терминале
celery -A procurement_system worker -l info
```

#### 2. Запуск Celery Beat (для периодических задач)

```bash
# В новом терминале
celery -A procurement_system beat -l info
```

#### 3. Запуск веб-сервера

```bash
# Для разработки
python manage.py runserver 0.0.0.0:8000

# Для production (используйте Gunicorn)
pip install gunicorn
gunicorn procurement_system.wsgi:application --bind 0.0.0.0:8000
```

### Docker развертывание

#### 1. Создание Docker образов

```bash
docker-compose build
```

#### 2. Запуск всех сервисов

```bash
docker-compose up -d
```

#### 3. Выполнение миграций в Docker

```bash
docker-compose exec web python manage.py migrate
```

#### 4. Создание суперпользователя в Docker

```bash
docker-compose exec web python manage.py createsuperuser
```

### Проверка API

#### 1. Регистрация пользователя

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

#### 2. Вход в систему

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### 3. Получение списка товаров

```bash
curl -X GET http://localhost:8000/api/products/products/ \
  -H "Authorization: Token <your_token>"
```

#### 4. Импорт товаров из YAML

```bash
curl -X POST http://localhost:8000/api/products/import/ \
  -H "Authorization: Token <your_token>" \
  -F "file=@shop_data.yaml" \
  -F "supplier_id=1"
```

### Структура проекта

```
procurement_system/
├── manage.py
├── requirements.txt
├── README.md
├── API_DOCUMENTATION.md
├── SETUP_INSTRUCTIONS.md
├── docker-compose.yml
├── Dockerfile
├── shop_data.yaml
├── .gitignore
├── procurement_system/          # Основные настройки Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── users/                      # Управление пользователями
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── contact_serializers.py
│   └── contact_views.py
├── products/                   # Управление товарами
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tasks.py
├── orders/                     # Управление заказами
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tasks.py
│   └── checkout_views.py
└── suppliers/                  # Управление поставщиками
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

### Возможные проблемы и решения

#### 1. Ошибка при миграциях

Если возникает ошибка при добавлении полей в существующие модели:

```bash
# Удалить миграции и создать заново
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

#### 2. Ошибка Redis

Если Redis не запущен:

```bash
# Проверить статус Redis
sudo service redis-server status

# Запустить Redis
sudo service redis-server start

# Установить Redis (если не установлен)
sudo apt-get install redis-server
```

#### 3. Ошибка импорта YAML

Если возникает ошибка кодировки при импорте:

```bash
# Убедитесь, что YAML файл в кодировке UTF-8
file -bi shop_data.yaml
```

#### 4. Проблемы с правами доступа

```bash
# Установить правильные права для проекта
chmod -R 755 .
chown -R $USER:$USER .
```

### Мониторинг и логирование

#### 1. Логи Django

```bash
# Просмотр логов
tail -f django.log
```

#### 2. Логи Celery

```bash
# В терминале с Celery worker
# Логи выводятся в консоль

# Для сохранения в файл
celery -A procurement_system worker -l info --logfile=celery.log
```

#### 3. Мониторинг Redis

```bash
# Проверка состояния Redis
redis-cli info
```

### Резервное копирование

#### 1. База данных PostgreSQL

```bash
pg_dump diplom_db > backup.sql
```

#### 2. База данных SQLite

```bash
cp db.sqlite3 backup.sqlite3
```

### Обновление проекта

```bash
# Получение обновлений
git pull origin main

# Обновление зависимостей
pip install -r requirements.txt

# Выполнение миграций
python manage.py migrate

# Перезапуск сервисов
sudo service restart celery
sudo service restart nginx  # если используется
```

### Поддержка

Для получения помощи:
1. Проверьте логи ошибок
2. Убедитесь, что все зависимости установлены
3. Проверьте конфигурацию переменных окружения
4. Ознакомьтесь с документацией API в `API_DOCUMENTATION.md`
