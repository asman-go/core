from pydantic_settings import BaseSettings
import pytest

from asman.core.adapters.db import DynamoDB, DynamoDBConfig


@pytest.fixture()
def dynamodb_config(monkeypatch):
    # YDB: via cli — ydb config profile get db1
    monkeypatch.setenv('DOCUMENT_API_ENDPOINT', 'https://example.com/path/to/your/db')
    monkeypatch.setenv('REGION_NAME', 'ru-central1')
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', '<key-id>')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', '<secret-access-key>')

    monkeypatch.setenv('SQS_SERVER_ENDPOINT', 'https://message-queue.api.cloud.yandex.net')
    monkeypatch.setenv('SQS_QUEUE_URL', '<???>')

    return DynamoDBConfig()


@pytest.fixture()
def dynamodb_table_name():
    """
        Таблица, в которой что-то храним в DynamoDB
    """
    return "example"


@pytest.fixture()
def dynamodb_key_schema():
    """
        Схема ключей таблицы dynamodb_table_name в DynamoDB
    """
    return [
        {
            'AttributeName': 'column1',
            'KeyType': 'HASH'
        }
    ]


@pytest.fixture()
def dynamodb_attribute_definitions():
    """
        Схема столбцов таблицы dynamodb_table_name в DynamoDB
    """
    return [
        {
            'AttributeName': 'column0',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'column1',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'column2',
            'AttributeType': 'S'
        }
    ]


@pytest.fixture()
def dynamodb(
            dynamodb_config,
            dynamodb_key_schema,
            dynamodb_attribute_definitions
        ):
    db = DynamoDB(
        dynamodb_config,
        dynamodb_key_schema,
        dynamodb_attribute_definitions,
    )

    return db
