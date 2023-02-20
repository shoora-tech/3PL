deps:
	pip install -r requirements.txt

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

shell:
	python manage.py shell

run:
	python manage.py runserver

startapp: 
	python manage.py startapp "$(app)"

containers:
	docker-compose up

format:
	black * --force-exclude="Makefile|.txt"

lint:
	black * --force-exclude="Makefile|.txt" --check
