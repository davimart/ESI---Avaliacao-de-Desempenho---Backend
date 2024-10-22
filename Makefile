PYTHON = python
MANAGE = $(PYTHON) manage.py
PORT = 8000
ENV = .env

help:
	@echo "Available commands:"
	@echo "  make runserver            - Run the Django development server"
	@echo "  make runserver-port       - Run the Django development server on a custom port"
	@echo "  make migrate              - Apply database migrations"
	@echo "  make makemigrations       - Create new database migrations based on models"
	@echo "  make superuser            - Create a superuser for the admin"
	@echo "  make shell                - Open Django shell"
	@echo "  make test                 - Run unit tests"
	@echo "  make clean-pyc            - Remove Python file artifacts"

runserver:
	$(MANAGE) runserver

runserver-port:
	$(MANAGE) runserver 0.0.0.0:$(PORT)

populate-db:
	python manage.py populate_db

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

test:
	$(MANAGE) test

clean-pyc:
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +

activate:
	source venv/bin/activate

migrate-app:
	$(MANAGE) makemigrations $(app)

custom-command:
	$(MANAGE) $(command)

.DEFAULT_GOAL := help