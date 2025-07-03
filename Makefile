dev: check migrate
	python manage.py runserver

check:
	python manage.py check

migrate: 
	python manage.py makemigrations
	python manage.py migrate

dump:
	python manage.py dumpdata user > .fixtures/user.json

load:
	python manage.py loaddata  .fixtures/data.json
