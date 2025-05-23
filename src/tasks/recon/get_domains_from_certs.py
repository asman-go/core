import asyncio
from celery import shared_task
from typing import Iterable, Dict, List

from asman.core.adapters.clients.crtsh import CrtshClient


@shared_task
async def get_domains_from_crtsh(domains: Iterable[str]):
    """
        Таска берет пачку доменов (domains) и идет с ними в crt.sh
        Из сертов вытаскивает новые домены и отдает их как есть
    """

    result: Dict[str, List[str]] = dict()

    async def get_certificates(client: CrtshClient, domain: str):
        certs = await client.get_certificates(domain)
        cert_domains = list()

        for cert in certs:
            cert_domains.extend([
                cert.common_name,
                *cert.name_value.split('\n'),
            ])

        result[domain] = list(set(cert_domains))  # unique

    async with CrtshClient() as crtsh_client:
        await asyncio.gather(*[get_certificates(crtsh_client, domain) for domain in domains])

    return result
