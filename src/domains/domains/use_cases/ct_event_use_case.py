from functools import reduce
from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.domains.api import (
    FacebookCtEvent,
)
from asman.domains.domains.repo import DomainRepository
from .utils import join


class NewCtEventUseCase(AbstractUseCase):
    def __init__(self, config: BaseSettings, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.repo = DomainRepository(database)

    async def execute(self, request: FacebookCtEvent) -> bool:
        changes = list()
        for entry in request.entry:
            changes.extend(entry.changes)

        data = reduce(
            join,
            map(
                lambda change: change.value,
                changes
            )
        )
        await self.repo.insert(data)

        return True
