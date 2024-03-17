from asman.core.arch import AbstractUseCase, RequestEntity
from asman.core.adapters.db import DynamoDB, DynamoDBConfig

from ..models import (
    PROGRAMMES_TABLE_KEY_SCHEMA,
    PROGRAMMES_TABLE_ATTRIBUTE_DEFINITIONS
)
from ..repo.repositories import BugBountyProgramRepository


class NewBugBountyProgramUseCase(AbstractUseCase):

    def __init__(self, config: DynamoDBConfig) -> None:
        database = DynamoDB(
            config,
            PROGRAMMES_TABLE_KEY_SCHEMA,
            PROGRAMMES_TABLE_ATTRIBUTE_DEFINITIONS
        )
        self.repo = BugBountyProgramRepository(database)

    def execute(self, request: RequestEntity):
        pass
