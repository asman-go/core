import pytest

from moto import mock_dynamodb
from pydantic_settings import BaseSettings

from src.domains.example.domain import Config
from src.core.adapters.db import MockDynamoDB, DynamoDBConfig
from src.domains.example.domain import ExampleEntity
from src.domains.example.domain import (
    DYNAMODB_TABLE_NAME,
    DYNAMODB_KEY_SCHEMA,
    DYNAMODB_ATTRIBUTE_DEFINITIONS,
)
from src.domains.example.repo import ExampleRepository


@pytest.fixture
def example_entity():
    return ExampleEntity(
        address='SOME_ADDRESS'
    )

@pytest.fixture
@mock_dynamodb
def example_repository(dynamodb, dynamodb_table_name):
    # print('example_repository', 'fixture', dynamodb)
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
# @mock_dynamodb
def dynamodb(dynamodb_config, dynamodb_key_schema, dynamodb_attribute_definitions):

    db = MockDynamoDB(
        dynamodb_config,
        dynamodb_key_schema,
        dynamodb_attribute_definitions,
    )

    # print('dynamodb', 'fixture', db)
    return db
