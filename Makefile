.PHONY: build up down stop restart logs shell migrate createsuperuser

# Construir a imagem Docker
build:
	docker-compose up --build -d

# Subir os containers
up:
	docker-compose up -d

# Derrubar os containers
down:
	docker-compose down -v

# Parar os containers sem removê-los
stop:
	docker-compose stop

# Reiniciar os containers
restart:
	docker-compose restart

# Ver logs do Django
logs:
	docker-compose logs -f web

# Entrar no shell do container Django
shell:
	docker-compose exec web sh

# Aplicar migrações no banco de dados
migrate:
	docker-compose exec web python manage.py migrate --noinput

# Criar um superusuário no Django
createsuperuser:
	docker-compose exec web python manage.py createsuperuser

format-py:
	black .
	isort .

check: lint format-check