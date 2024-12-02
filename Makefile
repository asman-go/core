deps:
	@echo 'Переустанавливаем зависимости'
	@python -m pip uninstall -y asman
	@python tools/generate.py
	@python -m pip install "."

t-deploy:
	@echo 'Поднимаем окружение для тестов'
	@docker compose -f local/docker-compose.yml build
	@docker compose -f local/docker-compose.yml up

test:
	@python -m pytest .
