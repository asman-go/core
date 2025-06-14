deps-client:
	@python -m pip install "."[client]

deps:
	@echo 'Переустанавливаем зависимости'
	@python -m pip uninstall -y asman
	# @python tools/generate.py
	@python -m pip install "."

test:
	@python -m pip install -r requirements.test.txt
	@python -m pytest .
