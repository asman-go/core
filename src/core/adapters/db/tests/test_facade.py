import pytest

from asman.core.adapters.db import Databases, DatabaseFacade
from asman.core.adapters.db.postgresql import Postgres
from asman.core.adapters.db.dynamodb import DynamoDB


TABLE_NAME = "example"


@pytest.mark.parametrize('database_type, database_class', [
    (Databases.PostgreSQL, Postgres),
    (Databases.DynamoDB, DynamoDB),
])
def test_facade_instance_create(database_type, database_class, init_postgres_envs, init_dynamodb_envs):
    facade = DatabaseFacade(database_type)

    assert facade
    assert isinstance(facade._database, database_class)
