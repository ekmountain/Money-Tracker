## Virtual Environment
python -m venv venv

venv\Scripts\activate

## Install Dependencies
pip install django psycopg2-binary pytest-django

pip install python-dotenv

## Requirements.txt
pip freeze > requirements.txt

pip install -r requirements.txt

## PostgreSQL

- NAME: money_tracker
- USER: postgres
- PASSWORD: 
- HOST: localhost
- PORT: 5432

## Django
django-admin startproject money_tracker .

python manage.py migrate


## Create a Django Superuser
python manage.py createsuperuser

