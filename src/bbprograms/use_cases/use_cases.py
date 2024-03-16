from ..domain import BugBountyProgramEntity
from src.core.models import Config
from src.core.arch import AbstractUseCase, RequestEntity
from src.core.adapters.db import DynamoDB

from ..models import (
    PROGRAMMES_TABLE_KEY_SCHEMA,
    PROGRAMMES_TABLE_ATTRIBUTE_DEFINITIONS
)
from ..repo import BugBountyProgramRepository


class NewBugBountyProgramUseCase(AbstractUseCase):

    def __init__(self, config: Config) -> None:
        database = DynamoDB(
            config,
            PROGRAMMES_TABLE_KEY_SCHEMA,
            PROGRAMMES_TABLE_ATTRIBUTE_DEFINITIONS
        )
        self.repo = BugBountyProgramRepository(database)

    def execute(self, request: RequestEntity):
        pass