build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

migrate:
	docker-compose run --rm web python manage.py migrate

makemigrations:
	docker-compose run --rm web python manage.py makemigrations

createsuperuser:
	docker-compose run --rm web python manage.py createsuperuser

collectstatic:
	docker-compose run --rm web python manage.py collectstatic --no-input

shell:
	docker-compose run --rm web python manage.py shell

logs:
	docker-compose logs -f web

pygments-css:
	pygmentize -S default -f html -a .codehilite > static/css/pygments.css

tailwind-install:
	docker-compose run --rm web python manage.py tailwind install

tailwind-build:
	docker-compose run --rm web python manage.py tailwind build
