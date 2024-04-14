from pydantic_settings import BaseSettings
import pytest

from asman.core.adapters.db import Postgres, PostgresConfig


@pytest.fixture()
def postgres_config(monkeypatch):
    monkeypatch.setenv('POSTGRES_DB', 'db')
    monkeypatch.setenv('POSTGRES_USER', 'user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'password')

    return PostgresConfig()


@pytest.fixture()
def postgres(postgres_config):
    return Postgres(postgres_config)
