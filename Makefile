.PHONY: install migrate run test check

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

test:
	pytest

check:
	python manage.py check
