.PHONY: help build up start stop restart clean logs install install-module db-create

help:
	@echo "Odoo Makefile - Available commands:"
	@echo "  make build         - Build, start, initialize DB and install module (everything)"
	@echo "  make up         - Start containers"
	@echo "  make start      - Start Odoo server"
	@echo "  make stop       - Stop containers"
	@echo "  make restart    - Restart containers"
	@echo "  make clean      - Remove containers and volumes"
	@echo "  make logs       - Show Odoo logs"
	@echo "  make db-create - Create odoo database"
	@echo "  make install    - Initialize database with base module"
	@echo "  make install-module - Install custom module"

build:
	docker-compose up -d
	@echo "Waiting for PostgreSQL to be healthy..."
	@sleep 5
	@echo "Creating database..."
	docker exec odoo-db psql -U odoo -d postgres -c "CREATE DATABASE odoo;" 2>/dev/null || true
	@echo "Installing base module..."
	docker exec odoo-app odoo -d odoo -i base --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo --stop-after-init
	@echo "Installing custom_partner_balance module..."
	docker exec odoo-app odoo -d odoo -i custom_partner_balance --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo --stop-after-init
	docker restart odoo-app
	@echo "Done! Odoo is ready at http://localhost:8069"
	@echo "Login: admin / admin"

up:
	docker-compose up -d

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose restart

clean:
	docker-compose down -v

logs:
	docker logs odoo-app -f

db-create:
	docker exec odoo-db psql -U odoo -d postgres -c "CREATE DATABASE odoo;"

install: db-create
	@echo "Installing base module..."
	docker exec odoo-app odoo -d odoo -i base --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo --stop-after-init

install-module:
	@echo "Installing custom_partner_balance module..."
	docker exec odoo-app odoo -d odoo -i custom_partner_balance --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo --stop-after-init
	docker restart odoo-app