import pytest

from asman.domains.example.domain.config import Config
from asman.core.adapters.db import DatabaseFacade, Databases
from asman.domains.example.domain.example_entity import ExampleEntity

from asman.domains.example.domain import TABLE_NAME
from asman.domains.example.repo.example_repository import ExampleRepository


@pytest.fixture
def example_entity():
    return ExampleEntity(
        address='SOME_ADDRESS'
    )


@pytest.fixture
def example_repository(dynamodb, dynamodb_table_name):
    return ExampleRepository(dynamodb, dynamodb_table_name)


@pytest.fixture
def usecase_config(monkeypatch):
    ENV_SOME_VALUE = '123456'
    monkeypatch.setenv('some_value', ENV_SOME_VALUE)

    config = Config()
    return config


@pytest.fixture
def dynamodb_table_name():
    """
        Таблица, в которой что-то храним в DynamoDB
    """
    return TABLE_NAME


@pytest.fixture
def init_dynamodb_config(monkeypatch):
    monkeypatch.setenv('DOCUMENT_API_ENDPOINT', 'http://localhost:8000')
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', '12345')


@pytest.fixture
def dynamodb(init_dynamodb_config) -> DatabaseFacade:
    return DatabaseFacade(
        Databases.DynamoDB,
        TABLE_NAME,
    )
