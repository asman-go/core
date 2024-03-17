from pydantic_settings import BaseSettings
import pytest

from asman.core.adapters.db import DynamoDB


class Config(BaseSettings):
    # YDB: via cli — ydb config profile get db1
    DOCUMENT_API_ENDPOINT: str = "https://example.com/path/to/your/db"
    REGION_NAME: str = "ru-central1"
    AWS_ACCESS_KEY_ID: str = "<key-id>"
    AWS_SECRET_ACCESS_KEY: str = "<secret-access-key>"

    SQS_SERVER_ENDPOINT: str = 'https://message-queue.api.cloud.yandex.net'
    SQS_QUEUE_URL: str = '<???>'


@pytest.fixture()
def dynamodb_config():
    return Config()


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
