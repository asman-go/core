from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DynamoDB, DynamoDBConfig

from ..domain.config import Config
from ..repo.example_repository import ExampleRepository
from ..domain.dynamodb_schema import (
    DYNAMODB_TABLE_NAME,
    DYNAMODB_KEY_SCHEMA,
    DYNAMODB_ATTRIBUTE_DEFINITIONS,
)

from ..api.schema import Request


class ExampleUseCase(AbstractUseCase):
    def __init__(self, config: Config, databaseConfig: DynamoDBConfig) -> None:
        database = DynamoDB(
            databaseConfig,
            DYNAMODB_KEY_SCHEMA,
            DYNAMODB_ATTRIBUTE_DEFINITIONS,
        )
        self.repo = ExampleRepository(database, DYNAMODB_TABLE_NAME)

    def execute(self, request: Request):
        return request.data
