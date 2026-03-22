# Документация API Сервиса для магазина

## Общее описание

Backend-приложение для автоматизации закупок в розничной сети с использованием Django Rest Framework.

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

## Пример использования в Postman

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
