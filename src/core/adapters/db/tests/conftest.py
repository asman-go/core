import pytest

from asman.core.adapters.db import Databases, DatabaseFacade

from asman.core.adapters.db.postgresql.tests import init_postgres_envs
from asman.core.adapters.db.dynamodb.tests import init_dynamodb_envs


@pytest.fixture
def postgres_facade(init_postgres_envs) -> DatabaseFacade:
    return DatabaseFacade(Databases.PostgreSQL)


@pytest.fixture
def dynamodb_facade(init_dynamodb_envs) -> DatabaseFacade:
    return DatabaseFacade(Databases.DynamoDB)
