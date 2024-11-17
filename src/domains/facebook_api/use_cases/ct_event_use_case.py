from functools import reduce
from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.facebook_api.api import (
    FacebookCtEvent,
)
from asman.domains.facebook_api.repo import DomainRepository
from .utils import join


class NewCtEventUseCase(AbstractUseCase):
    def __init__(self, config: BaseSettings, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.repo = DomainRepository(database)

    async def execute(self, request: FacebookCtEvent) -> bool:
        data = reduce(
            join,
            map(
                lambda entry: entry.changes,
                request.entry
            )
        )
        await self.repo.insert(data)

        return True
