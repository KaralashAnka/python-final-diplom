# Backend-приложение для автоматизации закупок в розничной сети

## Описание проекта

Django Rest Framework приложение для управления закупками в розничной сети. Проект реализует полный функционал для работы с каталогом товаров, заказами, поставщиками и клиентами через REST API.

## Основные возможности

- **Управление пользователями**: Регистрация, аутентификация, профили, адреса доставки
- **Каталог товаров**: Категории, настраиваемые характеристики, поиск и фильтрация
- **Корзина и заказы**: Добавление товаров, оформление заказов с email уведомлениями
- **Поставщики**: Управление поставщиками, прайс-листами, просмотр заказов
- **Импорт/экспорт**: Загрузка товаров из YAML файлов, экспорт каталога
- **Асинхронные задачи**: Email уведомления через Celery
- **Админ-панель**: Полное управление данными через Django Admin

## Технологический стек

- **Backend**: Django 6.0.3, Django Rest Framework 3.16.1
- **База данных**: PostgreSQL (production) / SQLite (development)
- **Асинхронные задачи**: Celery с Redis
- **Аутентификация**: Django Token Authentication
- **Документация**: Custom API documentation
- **Контейнеризация**: Docker & Docker Compose

## API Эндпоинты

### Аутентификация
- `POST /api/auth/register/` - Регистрация пользователя
- `POST /api/auth/login/` - Вход в систему
- `POST /api/auth/logout/` - Выход
- `GET /api/auth/profile/` - Профиль пользователя

### Товары
- `GET /api/products/products/` - Список товаров с фильтрацией
- `POST /api/products/import/` - Импорт товаров из YAML
- `GET /api/products/export/` - Экспорт товаров

### Корзина
- `GET /api/orders/cart/` - Получение корзины
- `POST /api/orders/cart/add-item/` - Добавление товара
- `POST /api/orders/cart/remove-item/` - Удаление товара
- `POST /api/orders/cart/clear/` - Очистка корзины

### Заказы
- `GET /api/orders/orders/` - История заказов
- `POST /api/orders/order-confirm/` - Подтверждение заказа
- `GET /api/orders/orders/{id}/` - Детали заказа

### Контакты
- `POST /api/auth/contacts/add/` - Добавление контактных данных
- `GET /api/auth/contacts/` - Список контактов

## Быстрый старт

### 1. Клонирование и установка

```bash
git clone <repository_url>
cd procurement_system
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 4. Запуск сервера

```bash
python manage.py runserver
```

### 5. Запуск Celery (для email уведомлений)

```bash
# В новом терминале
celery -A procurement_system worker -l info
```

## Docker развертывание

```bash
# Запуск всех сервисов
docker-compose up -d

# Выполнение миграций
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser
```

## Структура проекта

```
procurement_system/
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── shop_data.yaml          # Пример YAML для импорта
├── API_DOCUMENTATION.md     # Полная документация API
├── SETUP_INSTRUCTIONS.md   # Инструкции по установке
├── procurement_system/      # Основные настройки Django
├── users/                  # Управление пользователями
├── products/               # Управление товарами
├── orders/                 # Управление заказами
└── suppliers/              # Управление поставщиками
```

## Модели данных

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

## Импорт товаров из YAML

Проект поддерживает импорт товаров из YAML файлов в соответствии со спецификацией:

```yaml
shop: Связной
categories:
  - id: 224
    name: Смартфоны
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

## Email уведомления

Система автоматически отправляет email уведомления:
- Подтверждение заказа клиенту
- Уведомление администратору о новом заказе
- Ежедневные отчеты (настраиваются через Celery Beat)

## Админ-панель

Полнофункциональная админ-панель по адресу `/admin/`:
- Управление пользователями и правами доступа
- Управление каталогом товаров
- Обработка заказов
- Управление поставщиками
- Просмотр статистики

## API Документация

Полная документация API доступна в файле `API_DOCUMENTATION.md` и включает:
- Все эндпоинты с примерами запросов/ответов
- Форматы данных
- Аутентификация
- Обработка ошибок
- Примеры использования в Postman

## Тестирование

```bash
# Запуск тестов
python manage.py test

# Проверка системы
python manage.py check
```

## Разработка

### Добавление новых эндпоинтов

1. Создать/обновить модель в `models.py`
2. Обновить сериализатор в `serializers.py`
3. Добавить View в `views.py`
4. Обновить URL в `urls.py`
5. Выполнить миграции
6. Обновить документацию API

### Конфигурация

Основные настройки в `procurement_system/settings.py`:
- `DEBUG` - режим отладки
- `DATABASE_URL` - подключение к БД
- `CELERY_BROKER_URL` - подключение к Redis
- `EMAIL_*` - настройки email

## Производительность

Оптимизации для production:
- Кэширование Django
- Оптимизированные запросы к БД
- Асинхронные задачи для тяжелых операций
- Статические файлы через CDN
- Мониторинг через Django Debug Toolbar

## Безопасность

- Token аутентификация
- CORS настройки
- Валидация входных данных
- Защита от CSRF
- Настройки безопасности Django

## Лицензия

MIT License

## Поддержка

Для вопросов и поддержки:
1. Ознакомьтесь с `API_DOCUMENTATION.md`
2. Проверьте `SETUP_INSTRUCTIONS.md`
3. Изучите логи ошибок
4. Проверьте конфигурацию окружения

---

**Проект полностью готов к использованию и соответствует требованиям дипломной работы по автоматизации закупок в розничной сети.**
