# Backend-приложение для автоматизации закупок

## Описание проекта

Система автоматизации закупок для розничных сетей, разработанная на Django Rest Framework. Приложение предоставляет REST API для управления заказами, товарами, поставщиками и пользователями.

## Основные возможности

- **Управление пользователями**: Регистрация, авторизация, управление профилем
- **Каталог товаров**: Управление категориями, товарами и их характеристиками
- **Корзина и заказы**: Добавление товаров в корзину, оформление заказов
- **Управление поставщиками**: Регистрация поставщиков, управление прайс-листами
- **Импорт товаров**: Загрузка товаров из YAML файлов
- **Email уведомления**: Отправка подтверждений заказов

## Технологический стек

- **Backend**: Django 6.0.3, Django Rest Framework 3.16.1
- **База данных**: SQLite (для разработки), PostgreSQL (для продакшена)
- **Асинхронные задачи**: Celery с Redis
- **Аутентификация**: Token Authentication
- **Фильтрация**: django-filter

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd procurement_system
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
venv\Scripts\activate  # Для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### 5. Миграции базы данных

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера

```bash
python manage.py runserver
```

## API Эндпоинты

### Аутентификация
- `POST /api/auth/register/` - Регистрация пользователя
- `POST /api/auth/login/` - Вход в систему
- `POST /api/auth/logout/` - Выход из системы
- `GET/PUT /api/auth/profile/` - Управление профилем
- `GET/POST /api/auth/addresses/` - Управление адресами доставки

### Товары
- `GET /api/products/products/` - Получение списка товаров
- `GET /api/products/products/{id}/` - Получение информации о товаре
- `GET/POST /api/products/categories/` - Управление категориями
- `GET/POST /api/products/attributes/` - Управление характеристиками товаров
- `POST /api/products/import/` - Импорт товаров
- `GET /api/products/export/` - Экспорт товаров

### Заказы
- `GET /api/orders/cart/` - Получение корзины
- `POST /api/orders/cart/add-item/` - Добавление товара в корзину
- `DELETE /api/orders/cart/remove-item/` - Удаление товара из корзины
- `POST /api/orders/checkout/` - Оформление заказа
- `GET /api/orders/orders/` - Получение списка заказов
- `GET /api/orders/orders/{id}/` - Получение деталей заказа

### Поставщики
- `GET/POST /api/suppliers/suppliers/` - Управление поставщиками
- `GET /api/suppliers/suppliers/{id}/orders/` - Получение заказов поставщика
- `GET/POST /api/suppliers/price-lists/` - Управление прайс-листами

## Структура проекта

```
procurement_system/
├── manage.py
├── procurement_system/         # Основные настройки проекта
├── users/                      # Управление пользователями
├── products/                   # Управление товарами
├── orders/                     # Управление заказами
├── suppliers/                  # Управление поставщиками
├── requirements.txt
└── README.md
```

## Модели данных

### Пользователи (Users)
- **User**: Расширенная модель пользователя с типами (клиент, поставщик, администратор)
- **Address**: Адреса доставки пользователей

### Товары (Products)
- **Category**: Категории товаров с поддержкой иерархии
- **Product**: Товары с ценами, остатками и характеристиками
- **ProductAttribute**: Настраиваемые характеристики товаров
- **ProductAttributeValue**: Значения характеристик для конкретных товаров

### Заказы (Orders)
- **Cart**: Корзина пользователя
- **CartItem**: Товары в корзине
- **Order**: Заказы пользователей
- **OrderItem**: Товары в заказе

### Поставщики (Suppliers)
- **Supplier**: Информация о поставщиках
- **PriceList**: Прайс-листы поставщиков

## Админ-панель

Админ-панель доступна по адресу `/admin/` и предоставляет интерфейс для управления:
- Пользователями и их профилями
- Товарами и категориями
- Заказами и корзинами
- Поставщиками и прайс-листами

## Разработка

### Запуск Redis (для Celery)

```bash
redis-server
```

### Запуск Celery worker

```bash
celery -A procurement_system worker -l info
```

### Запуск Celery beat (для периодических задач)

```bash
celery -A procurement_system beat -l info
```

## Тестирование

Запуск тестов:

```bash
python manage.py test
```

## Деплой

Для продакшена рекомендуется использовать:
- PostgreSQL в качестве базы данных
- Nginx в качестве веб-сервера
- Gunicorn в качестве WSGI сервера
- Redis для Celery и кеширования

## Лицензия

MIT License
