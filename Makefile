install:
	poetry install

dev:
	poetry run python manage.py runserver

build:
	poetry build

publish:
	poetry publish --dry-run

test:
	poetry run python manage.py test -v 2

lint:
	poetry run flake8 task_manager

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi