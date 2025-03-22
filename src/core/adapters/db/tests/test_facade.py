import pytest

from asman.core.adapters.db import Databases, DatabaseFacade
from asman.core.adapters.db.postgresql import Postgres
from asman.core.adapters.db.dynamodb import DynamoDB


TABLE_NAME = "example"


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
