DOCKER_COMPOSE := $(shell if docker compose version >/dev/null 2>&1; then echo "docker compose"; else echo "docker-compose"; fi)

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

live-build:
	$(DOCKER_COMPOSE) -f docker-compose.yml up -d --build

live:
	$(DOCKER_COMPOSE) -f docker-compose.yml up -d

down:
	$(DOCKER_COMPOSE) -f docker-compose.yml down

downv:
	$(DOCKER_COMPOSE) -f docker-compose.yml down -v

restart:
	$(DOCKER_COMPOSE) restart

migrate:
	$(DOCKER_COMPOSE) exec -it django python manage.py migrate

makemigrations:
	$(DOCKER_COMPOSE) exec -it django python manage.py makemigrations

mergemigrations:
	$(DOCKER_COMPOSE) exec -it django python manage.py makemigrations --merge

collectstatic:
	$(DOCKER_COMPOSE) exec -it django python manage.py collectstatic

createsuperuser:
	$(DOCKER_COMPOSE) exec django python manage.py createsuperuser

dump-restore:
	$(DOCKER_COMPOSE) exec -T postgresql /bin/bash -c "psql --username postgres postgres" < ./dump.sql
