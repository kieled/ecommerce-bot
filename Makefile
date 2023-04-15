#!/usr/bin/make

include .env

add-dev-migration:
	docker compose -f docker-compose-dev.yml exec fastapi_server alembic revision --autogenerate && \
	docker compose -f docker-compose-dev.yml exec fastapi_server alembic upgrade head && \
	echo "Migration added and applied."

run-dev-build:
	docker compose up --build -d

run-dev:
	docker compose up -d

stop-dev:
	docker compose down

formatter:
	cd backend/app && \
	poetry run black app