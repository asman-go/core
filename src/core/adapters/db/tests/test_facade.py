import pytest

from asman.core.adapters.db import Databases, DatabaseFacade
from asman.core.adapters.db.postgresql import Postgres
from asman.core.adapters.db.dynamodb import DynamoDB


TABLE_NAME = "example"


@pytest.fixture
def init_postgres_envs(monkeypatch):
    monkeypatch.setenv('POSTGRES_DB', 'my_db')
    monkeypatch.setenv('POSTGRES_USER', 'my_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'my_password')
    monkeypatch.setenv('POSTGRES_HOST', 'localhost')
    monkeypatch.setenv('POSTGRES_PORT', '6432')


@pytest.fixture
def init_dynamodb_envs(monkeypatch):
    monkeypatch.setenv('DOCUMENT_API_ENDPOINT', 'http://localhost:8000')
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', '12345')


@pytest.fixture
def postgres_facade(init_postgres_envs) -> DatabaseFacade:
    return DatabaseFacade(Databases.PostgreSQL)


@pytest.fixture
def dynamodb_facade(init_dynamodb_envs) -> DatabaseFacade:
    return DatabaseFacade(Databases.DynamoDB)


@pytest.mark.parametrize('database_type, database_class, table_name', [
    (Databases.PostgreSQL, Postgres, None),
    (Databases.PostgreSQL, Postgres, TABLE_NAME),
    (Databases.DynamoDB, DynamoDB, None),
    (Databases.DynamoDB, DynamoDB, TABLE_NAME),
])
def test_facade_instance_create(database_type, database_class, table_name, init_postgres_envs, init_dynamodb_envs):
    facade = DatabaseFacade(database_type, table_name)

    assert facade
    assert isinstance(facade._database, database_class)
    assert facade._table_name == table_name
