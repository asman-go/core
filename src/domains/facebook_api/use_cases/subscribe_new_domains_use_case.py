import asyncio
from typing import List, Dict

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.facebook_api.repo import DomainRepository
from asman.core.adapters.clients.facebook import (
    FacebookConfig,
    FacebookGraph,
)


class SubscribeNewDomainsUseCase(AbstractUseCase):
    def __init__(self, config: FacebookConfig, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.config = config
        self.repo = DomainRepository(database)

    async def execute(self, domains: List[str]) -> List[str]:
        # TODO: записывать в бд статус домена — мы подписались
        result: Dict[str, List[str]] = dict()

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
            await fb_client.subscribe(domains)

        # 3. Save results
        self.repo.insert(result)

        return result.keys()
