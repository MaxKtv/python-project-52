### Hexlet tests and linter status:
[![Actions Status](https://github.com/MaxKtv/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/MaxKtv/python-project-52/actions)
[![Python CI](https://github.com/MaxKtv/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/MaxKtv/python-project-52/actions/workflows/pyci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/6d2f0574aeced1b090da/maintainability)](https://codeclimate.com/github/MaxKtv/python-project-52/maintainability)

# Task Manager

A simple and flexible task management web application.

## About

Task Manager is a web application built with Python and Django. It enables users to manage tasks efficiently, providing features to create, assign, and track tasks. The application supports user registration and authentication and uses a modern interface powered by Bootstrap.

The backend renders the frontend using Django Templates. PostgreSQL is the primary database, and the application is ready for easy deployment.

## Features

- Create and manage tasks.
- Assign tasks to performers.
- Change task statuses.
- Add multiple labels to tasks.
- Filter tasks by various criteria (status, performer, label, etc.).
- User registration and authentication.

## Built With

- Python
- Django
- PostgreSQL
- Bootstrap
- Poetry
- Gunicorn
- Whitenoise
- Rollbar

## Installation

### Prerequisites

- Python 3.10+
- Poetry
- PostgreSQL or SQLite

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/MaxKtv/python-project-52.git
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Create a `.env` file in the root directory with the following variables:

   ```env
   DATABASE_URL=postgresql://{user}:{password}@{host}:{port}/{db}
   SECRET_KEY=your_secret_key
   ```

   If you're using SQLite, omit the `DATABASE_URL` variable and Django will default to SQLite.

4. Run database migrations:

   ```bash
   poetry run python manage.py migrate
   ```

5. Start the development server:

   ```bash
   poetry run python manage.py runserver
   ```

Access the app at `http://127.0.0.1:8000`.

## Usage

### Available Actions

1. **Registration**: Register to access the application.
2. **Authentication**: Log in to view and manage tasks.
3. **Users**: View all registered users. Update or delete your profile.
4. **Statuses**: Manage task statuses (create, update, delete).
5. **Labels**: Add, update, and delete labels.
6. **Tasks**: Create, update, delete, and filter tasks.


### Demo

[Live Demo](https://python-project-52-hhf9.onrender.com)

## Additional Information


### Development Tools

- Flake8: Linter for Python.
- Ruff: Python linter and code formatter

### Makefile Commands

- `make install`: Install dependencies
- `make start`: Start the server
- `make dev`: Start the development server
- `make lint`: Run Flake8 linter
