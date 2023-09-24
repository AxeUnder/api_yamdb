# api_yamdb

Это api-приложение, которое позволяет отправлять запросы (GET, POST, PATCH и DELETE) на сервер к базе данных для изменения записей о произведениях, их рейтинга и отзывов с комментариями к ним.
Можно запросить список произведений, пользователей, отзывов или авторизовавшись опубликовать собственный и дать оценку произведению.

**Использованные технологии:** #Python #Django #Djangorestframework #Djangorestframework-simplejwt #Pillow #PyJWT #django-filter #isort #requests

## Примеры запросов
Регистрация нового пользователя:
**POST** `/api/v1/auth/signup/`
```json
{
  "email": "user@example.com",
  "username": "string"
}
```

Получение списка всех категорий:
**GET** `api/v1/categories/`

Удаление жанра:
**DELETE** `/api/v1/genres/{slug}/`

Частичное обновление информации о произведении:
**PATCH** `/api/v1/titles/{titles_id}/`
```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Получение отзыва по id:
**GET** `/api/v1/titles/{title_id}/reviews/{review_id}/`

Добавление комментария к отзыву:
**POST** `/api/v1/titles/{title_id}/reviews/{review_id}/comments/`
```json
{
  "text": "string"
}
```

Получение списка всех пользователей:
**GET** `/api/v1/users/`

Документация:
**GET** `/redoc/`


## Запуск management команды по импорту csv Файлов
```bash
py manage.py import_csv
``` 

## Запуск проекта на Windows OS
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/lioleg/api_yamdb.git
cd api_yambd
```

Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла **requirements.txt**:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:
```bash
python manage.py migrate
```

Запустить сервер:
```bash
cd api_yambd
python manage.py runserver
```

## Об авторах
Python-разработчики
>[AxeUnder](https://github.com/AxeUnder),
>[Khatkovskii](https://github.com/Khatkovskii),
>[lioleg](https://github.com/lioleg).
