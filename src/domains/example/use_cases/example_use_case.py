from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from ..domain.config import Config
from ..repo.example_repository import ExampleRepository
from ..domain import TABLE_NAME

from ..api.schema import Request


class ExampleUseCase(AbstractUseCase):
    def __init__(self, config: Config) -> None:
        assert config.value == '123456'
        self.repo = ExampleRepository(DatabaseFacade(Databases.DynamoDB), TABLE_NAME)

    def execute(self, request: Request):
        return request.data
