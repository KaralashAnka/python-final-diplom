# Backend-приложение для автоматизации закупок в розничной сети

## Описание проекта

Django Rest Framework приложение для управления закупками в розничной сети. Проект реализует полный функционал для работы с каталогом товаров, заказами, поставщиками и клиентами через REST API.

## Основные возможности

- **Управление пользователями**: Регистрация, аутентификация, профили, адреса доставки
- **Каталог товаров**: Категории, настраиваемые характеристики, поиск и фильтрация
- **Корзина и заказы**: Добавление товаров, оформление заказов
- **Поставщики**: Управление поставщиками, прайс-листами, просмотр заказов
- **Импорт/экспорт**: Загрузка товаров из YAML файлов, экспорт каталога
- **Асинхронные задачи**: Обработка фоновых операций через Celery
- **Админ-панель**: Полное управление данными через Django Admin

## Технологический стек

- **Backend**: Django 6.0.3, Django Rest Framework 3.16.1
- **База данных**: PostgreSQL (production) / SQLite (development)
- **Асинхронные задачи**: Celery с Redis
- **Аутентификация**: Django Token Authentication
- **Документация**: Custom API documentation
- **Контейнеризация**: Docker & Docker Compose

---

# 📋 ПОЛНАЯ ДОКУМЕНТАЦИЯ API

## Точки входа API сервиса

### Базовый URL: `http://localhost:8000/api/`

---

## 1. Аутентификация

### Вход (Login)

**POST** `/auth/login/`

**Аргументы для отправки API запроса:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Ответ:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "client"
    }
}
```

---

### Регистрация

**POST** `/auth/register/`

**Аргументы для отправки API запроса:**
```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Ответ:**
```json
{
    "id": 2,
    "username": "newuser",
    "email": "newuser@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "client"
}
```

---

## 2. Товары

### Запрос списка товаров с возможностью фильтрации и поиска

**GET** `/products/products/`

**Параметры запроса:**
- `search` - поиск по наименованию и описанию
- `category` - фильтрация по категории
- `supplier` - фильтрация по поставщику
- `ordering` - сортировка (price, -price, created_at, -created_at)

**JSON поля товара:**
```json
{
    "id": 1,
    "name": "Смартфон Apple iPhone XS Max 512GB (золотистый)",
    "description": "Описание товара",
    "model": "apple/iphone/xs-max",
    "sku": "4216292",
    "category": {
        "id": 1,
        "name": "Смартфоны"
    },
    "supplier": {
        "id": 1,
        "company_name": "Связной"
    },
    "price": 110000.00,
    "price_rrc": 116990.00,
    "stock_quantity": 14,
    "is_active": true,
    "attributes": [
        {
            "attribute_name": "Диагональ (дюйм)",
            "value": "6.5"
        },
        {
            "attribute_name": "Разрешение (пикс)",
            "value": "2688x1242"
        },
        {
            "attribute_name": "Встроенная память (Гб)",
            "value": "512"
        },
        {
            "attribute_name": "Цвет",
            "value": "золотистый"
        }
    ]
}
```

---

## 3. Корзина

### Получение корзины

**GET** `/orders/cart/`

**Список товаров с полями:**
```json
{
    "id": 1,
    "items": [
        {
            "id": 1,
            "product_name": "Смартфон Apple iPhone XS Max 512GB (золотистый)",
            "supplier_name": "Связной",
            "quantity": 2,
            "price": 110000.00,
            "total_price": 220000.00
        }
    ],
    "total_price": 220000.00
}
```

### Добавление товара в корзину

**POST** `/orders/cart/add-item/`

```json
{
    "product_id": 1,
    "quantity": 2
}
```

### Удаление товара из корзины

**POST** `/orders/cart/remove-item/`

```json
{
    "product_id": 1
}
```

### Очистка корзины

**POST** `/orders/cart/clear/`

---

## 4. Контакты

### API запрос добавления контакта

**POST** `/auth/contacts/add/`

**Аргументы для отправки:**
```json
{
    "first_name": "Иван",
    "last_name": "Иванов",
    "middle_name": "Иванович",
    "email": "ivan@example.com",
    "phone": "+71234567890",
    "city": "Москва",
    "street": "Тверская улица",
    "house": "1",
    "building": "А",
    "structure": "",
    "apartment": "123",
    "is_default": true
}
```

**Ответ:**
```json
{
    "id": 1,
    "first_name": "Иван",
    "last_name": "Иванов",
    "middle_name": "Иванович",
    "email": "ivan@example.com",
    "phone": "+71234567890",
    "city": "Москва",
    "street": "Тверская улица",
    "house": "1",
    "building": "А",
    "structure": "",
    "apartment": "123",
    "is_default": true
}
```

---

## 5. Заказы

### API запрос на подтверждение заказа

**POST** `/orders/order-confirm/`

**Аргументы:**
```json
{
    "cart_id": 1,
    "contact_id": 1
}
```

**Ответ:**
```json
{
    "message": "Заказ успешно оформлен",
    "order_id": 1,
    "order_number": "ORD-20231201-001",
    "total_amount": 220000.00,
    "status": "pending"
}
```

### Получение статуса и истории заказов

**GET** `/orders/orders/`

**Поля заказа:**
```json
{
    "id": 1,
    "order_number": "ORD-20231201-001",
    "status": "pending",
    "total_amount": 220000.00,
    "created_at": "2023-12-01T12:00:00Z",
    "items": [
        {
            "product_name": "Смартфон Apple iPhone XS Max 512GB (золотистый)",
            "supplier_name": "Связной",
            "quantity": 2,
            "price": 110000.00,
            "total_price": 220000.00
        }
    ],
    "shipping_address_details": {
        "street": "Тверская улица",
        "city": "Москва",
        "postal_code": "123456",
        "country": "Russia"
    }
}
```

---

## 6. Импорт товаров

### Загрузка YAML файла с товарами

**POST** `/products/import/`

**Формат данных:**
- `file` - YAML файл с товарами
- `supplier_id` - ID поставщика

**Формат YAML файла:**
```yaml
shop: Связной
categories:
  - id: 224
    name: Смартфоны
  - id: 15
    name: Аксессуары

goods:
  - id: 4216292
    category: 224
    model: apple/iphone/xs-max
    name: Смартфон Apple iPhone XS Max 512GB (золотистый)
    price: 110000
    price_rrc: 116990
    quantity: 14
    parameters:
      "Диагональ (дюйм)": 6.5
      "Разрешение (пикс)": 2688x1242
      "Встроенная память (Гб)": 512
      "Цвет": золотистый
```

---

## 7. Статусы заказов

- `pending` - Ожидает обработки
- `confirmed` - Подтвержден
- `processing` - В обработке
- `shipped` - Отправлен
- `delivered` - Доставлен
- `cancelled` - Отменен

---

## 8. Типы пользователей

- `client` - Клиент
- `supplier` - Поставщик  
- `admin` - Администратор

---

## 9. Аутентификация

Для доступа к защищенным эндпоинтам необходимо использовать Token аутентификацию:

**Header:** `Authorization: Token <your_token>`

---

## 10. Ошибки

**400 Bad Request** - Неверные данные запроса
**401 Unauthorized** - Требуется аутентификация
**403 Forbidden** - Недостаточно прав
**404 Not Found** - Ресурс не найден
**500 Internal Server Error** - Внутренняя ошибка сервера

---

## 11. Пример использования в Postman

1. **Регистрация пользователя:**
   - Method: POST
   - URL: `http://localhost:8000/api/auth/register/`
   - Body: JSON с данными регистрации

2. **Вход в систему:**
   - Method: POST  
   - URL: `http://localhost:8000/api/auth/login/`
   - Body: JSON с email и паролем

3. **Получение списка товаров:**
   - Method: GET
   - URL: `http://localhost:8000/api/products/products/`
   - Headers: `Authorization: Token <token>`

4. **Добавление в корзину:**
   - Method: POST
   - URL: `http://localhost:8000/api/orders/cart/add-item/`
   - Headers: `Authorization: Token <token>`
   - Body: JSON с product_id и quantity

5. **Оформление заказа:**
   - Method: POST
   - URL: `http://localhost:8000/api/orders/order-confirm/`
   - Headers: `Authorization: Token <token>`
   - Body: JSON с cart_id и contact_id

---

# 🚀 ИНСТРУКЦИИ ПО УСТАНОВКЕ И ЗАПУСКУ

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

---

# 📁 СТРУКТУРА ПРОЕКТА

```
procurement_system/
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── shop_data.yaml          # Пример YAML для импорта
├── README.md  # Этот файл
├── API_DOCUMENTATION.md     # Отдельная документация API
├── SETUP_INSTRUCTIONS.md   # Отдельные инструкции
├── procurement_system/      # Основные настройки Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── users/                  # Управление пользователями
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── contact_serializers.py
│   └── contact_views.py
├── products/               # Управление товарами
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tasks.py
├── orders/                 # Управление заказами
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tasks.py
│   └── checkout_views.py
└── suppliers/              # Управление поставщиками
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

---

# 🔧 МОДЕЛИ ДАННЫХ

### Пользователи и адреса
- **User**: Расширенная модель пользователя с типами (client, supplier, admin)
- **Address**: Полные контактные данные с адресом доставки

### Товары
- **Category**: Иерархические категории товаров
- **Product**: Товары с характеристиками, ценами и остатками
- **ProductAttribute**: Настраиваемые характеристики товаров
- **ProductAttributeValue**: Значения характеристик для конкретных товаров

### Заказы
- **Cart**: Корзина пользователя
- **CartItem**: Товары в корзине
- **Order**: Заказы со статусами
- **OrderItem**: Товары в заказе

### Поставщики
- **Supplier**: Информация о поставщиках
- **PriceList**: Прайс-листы поставщиков

# 🎓 СООТВЕТСТВИЕ ТРЕБОВАНИЯМ ДИПЛОМНОЙ РАБОТЫ

## ✅ Основные требования реализованы:

- **Backend для procurement order service** на Django Rest Framework
- **Кастомная модель User** с типами (client, supplier, admin)  
- **Управление поставщиками** и прайс-листами
- **Каталог товаров** с категориями и характеристиками
- **Импорт товаров из YAML** согласно спецификации
- **Корзина и управление заказами**
- **Аутентификация** через API
- **Админ-панель** для всех моделей

## ✅ Дополнительные возможности:

- **Git** с регулярными коммитами
- **Импорт из YAML** с указанным форматом
- **Экспорт товаров** и управление статусами заказов
- **Асинхронные задачи** для медленных методов
- **Docker-compose** и инструкции по развертыванию
- **REST API** взаимодействие
- **Python 3.11+** совместимость
- **Использование AI инструментов** разрешено
- **Отсутствие плагиата** и творческий подход

---

