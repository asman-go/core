from src.core.arch import AbstractUseCase
from src.core.adapters.db import DynamoDB, DynamoDBConfig

from ..domain import Config
from ..repo import ExampleRepository
from ..domain import (
    DYNAMODB_TABLE_NAME,
    DYNAMODB_KEY_SCHEMA,
    DYNAMODB_ATTRIBUTE_DEFINITIONS,
)

from ..api.schema_pb2 import Request


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
