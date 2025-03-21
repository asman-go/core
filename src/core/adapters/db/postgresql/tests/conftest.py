import pytest

from asman.core.adapters.db.postgresql import Postgres, TableBase


@pytest.fixture
def init_postgres_envs(monkeypatch):
    monkeypatch.setenv('POSTGRES_DB', 'my_db')
    monkeypatch.setenv('POSTGRES_USER', 'my_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'my_password')
    monkeypatch.setenv('POSTGRES_HOST', 'localhost')
    monkeypatch.setenv('POSTGRES_PORT', '6432')


@pytest.fixture
def postgres_instance(init_postgres_envs) -> Postgres:
    return Postgres()
