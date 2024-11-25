install:
	poetry install

dev:
	poetry run python manage.py runserver

build:
	poetry build

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 task_manager

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

test:
	poetry run pytest

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi