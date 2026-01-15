


## Технологии / Зависимости
- Python 3.10–3.12
- Django 5.2
- PostgreSQL
- psycopg2-binary

## Быстрый старт (Windows)

###  Создай базу данных

Через pgAdmin или в командной строке:

```bash
# Через командную строку (если psql в PATH)
psql -U postgres

# Внутри psql выполнить:
CREATE DATABASE "disco-db";

git clone <твой-репозиторий>
cd <имя-папки-проекта>  

# Создать виртуальное окружение
python -m venv venv

# Активировать (ВАЖНО делать это каждый раз при открытии новой консоли!)
venv\Scripts\activate 

pip install -r requirements.txt  

# Применяем миграции
python manage.py migrate

#  создаём супер-пользователя(для входа в admin)
python manage.py createsuperuser

# Запускаем сервер
python manage.py runserver


## Для запуска сбора статистики flask 
cd flask 

venv\Scripts\activate

pip install -r requirements.txt

python app.py 



