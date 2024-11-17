import asyncio
from typing import List, Dict

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.facebook_api.repo import DomainRepository
from asman.core.adapters.clients.facebook import (
    FacebookConfig,
    FacebookGraph,
)


class UnsubscribeDomainsUseCase(AbstractUseCase):
    def __init__(self, config: FacebookConfig, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.config = config
        self.repo = DomainRepository(database)

    async def execute(self, domains: List[str]) -> bool:
        # TODO: записывать в бд статус домена — мы отписались

        async with FacebookGraph('https://graph.facebook.com', self.config) as fb_client:
            return await fb_client.unsubscribe(domains)
