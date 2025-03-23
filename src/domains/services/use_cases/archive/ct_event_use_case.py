from functools import reduce

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.services.api import (
    FacebookCtEvent,
)
from asman.domains.services.repo import DomainRepository
from asman.domains.services.utils import join
from asman.domains.services.domain import TABLE_DOMAINS_NAME


class NewCtEventUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = DomainRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_DOMAINS_NAME,
        )

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
