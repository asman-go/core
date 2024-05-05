from pydantic_settings import BaseSettings

import pytest

from asman.core.adapters.db import Postgres, PostgresConfig


# test_db = factories.postgresql_proc(port=None, dbname='my_db')

@pytest.fixture()
def postgres_config(monkeypatch) -> PostgresConfig:
    monkeypatch.setenv('POSTGRES_DB', 'my_db')
    monkeypatch.setenv('POSTGRES_USER', 'my_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'my_password')
    monkeypatch.setenv('POSTGRES_HOST', 'localhost')
    monkeypatch.setenv('POSTGRES_PORT', '5432')

    return PostgresConfig()


@pytest.fixture()
def postgres(postgres_config):
    return Postgres(postgres_config)


@pytest.fixture()
def db_in_memory():
    # https://mingzhi2.medium.com/how-to-create-a-test-database-pytest-pytest-postgresql-sqlalchemy-77f814b57b10

    # with DatabaseJanitor(
    #     user=postgres_config.POSTGRES_USER,
    #     host=postgres_config.POSTGRES_HOST,
    #     port=postgres_config.POSTGRES_PORT,
    #     version=test_db.version,
    #     dbname=postgres_config.POSTGRES_DB,
    #     password=postgres_config.POSTGRES_PASSWORD,
    # ):
    #     yield Postgres(postgres_config)

    return Postgres(None)
