import pytest
from sqlalchemy.exc import IntegrityError

from asman.domains.facebook_api.repo import DomainRepository


def test_domain_repository_instance_create(db_in_memory):
    repo = DomainRepository(db_in_memory)

    assert repo


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
    await domain_repository.insert(data)

    domains = await domain_repository.list('example.com')

    assert domains, 'Parent domain and subdomains were not added'
    assert len(domains) > 0, 'Can not list the parent domain and subdomains'

    await domain_repository.delete('example.com')

    domains = await domain_repository.list('example.com')
    assert not domains, 'Parent domain and subdomains were not deleted'
    assert len(domains) == 0, 'Parent domain and subdomains were not deleted'


@pytest.mark.asyncio
async def test_domain_repository_double_insert(domain_repository: DomainRepository):
    """
        The composite of domain column and parent domain column is the primary key. Check insert same domains
    """
    data1 = {
        'example1.com': [
            'a.example1.com',
            'b.example1.com',
        ],
    }

    data2 = {
        'test1.com': [
            'a.test1.com',
            'a.example1.com',
        ]
    }
    await domain_repository.insert(data1)
    await domain_repository.insert(data2)

    domains1 = await domain_repository.list('example1.com')
    domains2 = await domain_repository.list('test1.com')

    assert domains1
    assert domains2

    await domain_repository.insert(data2), 'Не смогли добавить повторяющуюся запись (policy: do_nothing)'
