# 🚀 Быстрый запуск проекта

## Ручная установка (для Windows или в случае проблем со скриптом)

```bash
# Установка зависимостей
pip install -r requirements.txt

# Создание файла окружения
copy .env.example .env  # Windows
cp .env.example .env    # Linux/MacOS

# Выполнение миграций
python manage.py migrate

# Создание администратора
python manage.py createsuperuser
```

## Настройка PostgreSQL

Создайте новую базу данных:

```sql
CREATE DATABASE advertisements_db;
```

## Генерация токена пользователя

```bash
# Запуск локального сервера
python manage.py runserver

# Перейдите в админ-панель:
# http://localhost:8000/admin/

# Авторизуйтесь под суперпользователем
# Откройте раздел "Tokens" и создайте токен для нужного пользователя
```

## Проверка API

Для тестирования можно использовать файл `requests-examples.http` вместе с расширением REST Client для VS Code либо выполнить запросы через `curl`.

```bash
# Получение списка объявлений (без авторизации)
curl http://localhost:8000/api/advertisements/

# Создание нового объявления (требуется токен)
curl -X POST http://localhost:8000/api/advertisements/ \
  -H "Authorization: Token ВАШ_ТОКЕН" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "description": "Test", "status": "OPEN"}'
```

## Запуск тестов

```bash
python manage.py test
```

---

# 📁 Структура проекта

```text
advertisements_project/
├── manage.py                 # Основной файл управления Django
├── requirements.txt          # Список зависимостей
├── README.md                 # Документация проекта
├── requests-examples.http    # Примеры HTTP-запросов
├── advertisements/           # Основное приложение
│   ├── models.py             # Модели данных
│   ├── serializers.py        # Сериализаторы
│   ├── views.py              # Представления
│   ├── permissions.py        # Настройка прав доступа
│   ├── filters.py            # Фильтрация данных
│   ├── urls.py               # Маршруты API
│   ├── admin.py              # Конфигурация админ-панели
│   └── tests.py              # Тестирование
└── advertisements_project/   # Конфигурация проекта
    ├── settings.py
    └── urls.py
```

---

# ✅ Основной функционал

- ✅ Полный набор CRUD-операций для объявлений
- ✅ Авторизация по токену
- ✅ Система прав доступа (редактирование доступно только автору)
- ✅ Ограничение: максимум 10 активных объявлений на пользователя
- ✅ Фильтрация по статусу и дате публикации
- ✅ Ограничение частоты запросов (Rate Limiting)
  - 10 запросов/мин — для гостей
  - 20 запросов/мин — для авторизованных пользователей
- ✅ Поддержка пагинации
- ✅ Административная панель Django
- ✅ Набор тестов
- ✅ Подробная документация

---


---