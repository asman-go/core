# core
Asman core python library

## Develop usage

Tests:

```
python -m pytest .
python -m pytest src/tasks/recon/tests
python -m pytest -m "not inet" src/tasks/recon/tests  (запуск по маркерам и путям)
```

Для тестов нужна постгря локальная:

```
docker compose -f local/docker-compose.yml build
docker compose -f local/docker-compose.yml up
```

Install:

```
python generate.py
python -m pip install .
```

или одной командой переустановить локальный пакет:

```
python -m pip uninstall -y asman && python tools/generate.py && python -m pip install "."
```


Links:

- https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html#summary
- За основу конфигов брал https://github.com/getmoto/moto
- Про pyproject.toml: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
