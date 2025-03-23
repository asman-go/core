import asyncio
from pydantic_settings import BaseSettings
from typing import List, Dict

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.domains.repo import DomainRepository
from asman.core.adapters.clients.crtsh import CrtshClient


class DomainsFromCertsUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = DomainRepository(
            DatabaseFacade(Databases.PostgreSQL),
        )

    async def execute(self, domains: List[str]) -> List[str]:
        result: Dict[str, List[str]] = dict()

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

        await self.repo.insert(result)
        return result.keys()
