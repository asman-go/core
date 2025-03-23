import asyncio
from typing import List, Dict

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.services.repo import DomainRepository
from asman.domains.services.domain import TABLE_DOMAINS_NAME
from asman.core.adapters.clients.facebook import (
    FacebookConfig,
    FacebookGraph,
)


class SubscribeNewDomainsUseCase(AbstractUseCase):
    def __init__(self, config: FacebookConfig) -> None:
        self.config = config
        self.repo = DomainRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_DOMAINS_NAME,
        )

    async def execute(self, domains: List[str]) -> bool:
        # TODO: записывать в бд статус домена — мы подписались
        # result: Dict[str, List[str]] = dict()

        # 1. Get information from Facebook Graph API
        async with FacebookGraph('https://graph.facebook.com', self.config) as fb_client:
            # Из-за лимитов мы не можем так сделать: слишком много запросов на получение сертов с одного домена

            # async def get_certificates(domain: str):
            #     certs = await fb_client.get_certificates(domain)
            #     cert_domains = list()
            #     for cert in certs:
            #         cert_domains.extend(cert.domains)
            #     result[domain] = cert_domains

            # await asyncio.gather(*[get_certificates(domain) for domain in domains])

        # 2. If it is new domain we'll subscribe for updates
            return await fb_client.subscribe(domains)

        # 3. Save results
        # await self.repo.insert(result)        
        # return result.keys()
