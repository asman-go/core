import pytest

from asman.core.adapters.db.postgresql import Postgres, TableBase

from .models import (
    TABLE_CHILDREN_NAME,
    TABLE_DEBUG_NAME,
    TABLE_PARENTS_NAME,
    TABLE_PARENT_CHILD_ASSOCIATION_NAME,
)

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


@pytest.fixture(autouse=True)
def clear_table(postgres_instance):
    # Перед каждым тестом очищаем таблицы
    postgres_instance.delete_all(TABLE_PARENT_CHILD_ASSOCIATION_NAME)
    postgres_instance.delete_all(TABLE_CHILDREN_NAME)
    postgres_instance.delete_all(TABLE_PARENTS_NAME)
    postgres_instance.delete_all(TABLE_DEBUG_NAME)
