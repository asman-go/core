import asyncio
from pydantic_settings import BaseSettings
from typing import List, Dict

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.services.repo import DomainRepository
from asman.domains.services.api import Domain
from asman.domains.services.domain import TABLE_DOMAINS_NAME
from asman.core.adapters.clients.crtsh import CrtshClient
from asman.tasks.recon import ReconDomainsFromCertsTask


class DomainsFromCertsUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = DomainRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_DOMAINS_NAME,
        )

    async def execute(self, domains: List[str]) -> List[Domain]:
        result: Dict[str, List[str]] = dict()

        print('DomainsFromCertsUseCase inp', domains)

        _result = ReconDomainsFromCertsTask.delay(domains)
        result = _result.get()

        print('DomainsFromCertsUseCase out', result)

        return await self.repo.insert(result)

        async with CrtshClient() as crtsh_client:
            async def get_certificates(domain: str):
                certs = await crtsh_client.get_certificates(domain)
                cert_domains = list()
                for cert in certs:
                    cert_domains.extend(
                        [
                            cert.common_name,
                            *cert.name_value.split('\n')
                        ]
                    )
                result[domain] = list(set(cert_domains))  # unique

            await asyncio.gather(*[get_certificates(domain) for domain in domains])

        return await self.repo.insert(result)
