import pytest

from asman.domains.domains.repo import DomainRepository
from asman.domains.domains.api import SearchByDomain, SearchByParentDomain


@pytest.mark.asyncio
async def test_domain_repository_crud(domain_repository: DomainRepository):
    data = {
        'example.com': [
            'a.example.com',
            'b.example.com',
        ],
        'test.com': [
            'a.test.com',
            'b.test.com',
        ]
    }
    res = await domain_repository.insert(data)
    domains = await domain_repository.search([
        SearchByParentDomain(
            parent_domain='example.com'
        )
    ])

    assert domains, 'Parent domain and subdomains were not added'
    assert len(domains) > 0, 'Can not list the parent domain and subdomains'

    res = await domain_repository.delete([
        SearchByParentDomain(
            parent_domain='example.com'
        )
    ])
    domains = await domain_repository.search([
        SearchByParentDomain(
            parent_domain='example.com'
        )
    ])
    assert not domains, 'Parent domain and subdomains were not deleted'
    assert len(domains) == 0, 'Parent domain and subdomains were not deleted'
