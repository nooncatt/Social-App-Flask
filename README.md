# Social App (Flask)

Мини-API социальной сети для текстовых постов: пользователи, посты, реакции и лидерборд.

- Полное ТЗ перенесено сюда: **[docs/TECH_SPEC.md](./docs/TECH_SPEC.md)**

---

## Технологии

- Python 3.12
- Flask
- email-validator (проверка корректности e-mail)
- matplotlib (построение графика для лидерборда)

## Допущения и договорённости

- Данные хранятся **в памяти** процесса (runtime). После перезапуска приложения всё обнуляется.
- `user_id` и `post_id` — это **индексы** в списках `USERS` и `POSTS`. Удаления объектов нет, поэтому индексы стабильны.
- Один пользователь может оставить **ровно одну** реакцию на каждый пост (реакцию можно **сменить**).
- **Самолайк** разрешён и учитывается один раз, как и от любого пользователя.
- Форматирование кода — `black`.

---

## Установка и запуск

````
1) создать и активировать виртуальное окружение
python -m venv env
# Windows:
env\Scripts\activate
# macOS/Linux:
# source env/bin/activate

2) установить зависимости
pip install -r requirements.txt

3) запустить приложение
python run.py
# приложение будет доступно на http://127.0.0.1:5000
````

---

## Структура проекта

```
app/
  __init__.py        # Flask app, глобальные USERS/POSTS, импорт роутов и моделей
  models.py          # классы User и Post, валидации, логика реакций
  views/             # роуты (без blueprints)
    users.py         # /users/create, /users/<id>, /users/<id>/posts
    posts.py         # /posts/create, /posts/<id>
    reactions.py     # /posts/<id>/reaction
    leaderboard.py   # /users/leaderboard (type=list|graph, sort=asc|desc)
  static/            # сюда сохраняется PNG графика лидерборда
docs/
  TECH_SPEC.md       # полное техническое задание
run.py               # точка входа приложения
requirements.txt
```

---

## Эндпоинты (кратко)

* **POST `/users/create`** — создать пользователя (валидация e-mail).

  * Успех: `201 Created`
  * Ошибки: `404` (если e-mail невалиден по текущей логике), `409` (такой e-mail уже зарегистрирован)

* **GET `/users/<user_id>`** — получить пользователя.

  * Успех: `200 OK`
  * Ошибки: `404` (пользователь не найден)

* **POST `/posts/create`** — создать пост.

  * Успех: `201 Created`
  * Ошибки: `404` (автор не найден), `400` (пустой текст)

* **GET `/posts/<post_id>`** — получить пост.

  * Успех: `200 OK`
  * Ошибки: `400` (некорректный id поста)

* **POST `/posts/<post_id>/reaction`** — поставить/сменить реакцию.

  * Успех: `204 No Content`
  * Ошибки: `400` (некорректный id поста или реакция), `404` (пользователь не найден)

* **GET `/users/<user_id>/posts?sort=asc|desc`** — посты пользователя, отсортированные по количеству реакций.

  * Успех: `200 OK`
  * Ошибки: `400` (неверный параметр `sort`), `404` (пользователь не найден)

* **GET `/users/leaderboard?type=list|graph&sort=asc|desc`** — лидерборд пользователей по сумме полученных реакций.

  * `type=list` → JSON-список
  * `type=graph` → **HTML с `<img>`**, где `src` указывает на сохранённый PNG в `static/leaderboard_graph.png`
  * Ошибки: `400` (неверный `type`/`sort`), `404` (нет пользователей)

> Примечание по графику: текущая реализация сохраняет изображение в `app/static/leaderboard_graph.png` и возвращает HTML:
>
> ```html
> <img src="/static/leaderboard_graph.png">
> ```
>
> Это сделано для простоты проверки через браузер/Postman.

---


## Полезные команды

```bash
# форматирование кода
pip install black
black .

# обновить requirements.txt по текущему окружению
pip freeze > requirements.txt
```


