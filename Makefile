# dskgskfbgsd

deps:
	@echo 'Переустанавливаем зависимости'
	@python -m pip uninstall -y asman
	# @python tools/generate.py
	@python -m pip install "."

t-deploy:
	@echo 'Поднимаем окружение для тестов'
	# Останавливаем контейнеры, если запущены
	@docker compose -f local/docker-compose.yml down
	# Собираем и запускаем
	@docker compose -f local/docker-compose.yml build
	@docker compose -f local/docker-compose.yml up

test:
	@python -m pip install -r requirements.test.txt
	@python -m pytest .
