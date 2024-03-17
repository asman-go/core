import pytest

from domains.example.domain.config import Config
from core.adapters.db import MockDynamoDB, DynamoDBConfig
from domains.example.domain.example_entity import ExampleEntity

from domains.example.domain.dynamodb_schema import (
    DYNAMODB_TABLE_NAME,
    DYNAMODB_KEY_SCHEMA,
    DYNAMODB_ATTRIBUTE_DEFINITIONS,
)
from domains.example.repo.example_repository import ExampleRepository


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
    ENV_SOME_VALUE = 'testtest'
    monkeypatch.setenv('some_value', ENV_SOME_VALUE)

    config = Config()
    return config


@pytest.fixture
def dynamodb_table_name():
    """
        Таблица, в которой что-то храним в DynamoDB
    """
    return DYNAMODB_TABLE_NAME


@pytest.fixture
def dynamodb_key_schema():
    """
        Схема ключей таблицы dynamodb_table_name в DynamoDB
    """
    return DYNAMODB_KEY_SCHEMA


@pytest.fixture
def dynamodb_attribute_definitions():
    """
        Схема столбцов таблицы dynamodb_table_name в DynamoDB
    """
    return DYNAMODB_ATTRIBUTE_DEFINITIONS


@pytest.fixture
def dynamodb_config() -> DynamoDBConfig:
    return DynamoDBConfig()


@pytest.fixture
def dynamodb(
            dynamodb_config,
            dynamodb_key_schema,
            dynamodb_attribute_definitions
        ):

    db = MockDynamoDB(
        dynamodb_config,
        dynamodb_key_schema,
        dynamodb_attribute_definitions,
    )

    # print('dynamodb', 'fixture', db)
    return db
