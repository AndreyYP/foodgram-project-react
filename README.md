# Проект Foodgram
### Сайт позволяет делиться своими рецептами с людьми
# Адрес сайта - https://foodgramz.hopto.org/
# Данные для входа в админ панель:
### login: admin@mail.ru
### password: admin

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AndreyYP/foodgram-project-react.git
```

```
cd foodgram
```

Cоздать и активировать виртуальное окружение:

```
py -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
py manage.py migrate
```

Запустить проект через docker compose :

```
docker compose up --build
```
```
docker compose exec backend python manage.py collectstatic
```
Локально сайт будет доступен по адресу - http://127.0.0.1:8000/
