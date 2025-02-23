### Описание:

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/sejapoe/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv .venv
```

```
source .venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры API:

#### Получение публикаций | `GET /api/v1/posts`

Параметры запроса

- `limit` (integer, optional): Количество публикаций на страницу
- `offset` (integer, optional): Количество публикаций после которых начинать выдачу

Пример запроса:

```bash
GET /api/v1/posts/?limit=100&offset=300
```

Пример ответа:

```json
{
  "count": 123,
  "next": "http://localhost:8000/api/v1/posts/?offset=400&limit=100",
  "previous": "http://localhost:8000/api/v1/posts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "admin",
      "text": "Lorem ipsum dolor sit amet.",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "group": 7
    }
  ]
}
```

#### Создание публикаций | `POST /api/v/posts/`

Тело запроса

- `text` (string): текст публикации
- `image` (binary, optional): изображение к публикации
- `group` (integer, optional): ID сообщества, в котором сделана публикация

Пример запроса:

```
POST /api/v1/posts/
{
    "text": "Lorem ipsum dolor amet.",
    "image": "string",
    "group": 7
}
```

Пример ответа:
```json
{
  "id": 12,
  "author": "admin",
  "text": "Lorem ipsum dolor amet.",
  "pub_date": "2024-09-09T14:15:22Z",
  "image": null,
  "group": 7
}
```