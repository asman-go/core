from typing import List

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.services.repo import DomainRepository
from asman.domains.services.domain import TABLE_DOMAINS_NAME
from asman.core.adapters.clients.facebook import (
    FacebookConfig,
    FacebookGraph,
)


class UnsubscribeDomainsUseCase(AbstractUseCase):
    def __init__(self, config: FacebookConfig) -> None:
        self.config = config
        self.repo = DomainRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_DOMAINS_NAME,
        )

    async def execute(self, domains: List[str]) -> bool:
        # TODO: записывать в бд статус домена — мы отписались

        async with FacebookGraph('https://graph.facebook.com', self.config) as fb_client:
            return await fb_client.unsubscribe(domains)
