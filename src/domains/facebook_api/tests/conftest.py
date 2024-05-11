import pytest

from asman.core.adapters.tests import db_in_memory, postgres, postgres_config, facebook_config
from asman.domains.facebook_api.repo import DomainRepository
from asman.domains.facebook_api.use_cases import (
    NewCtEventUseCase,
    SubscribeNewDomainsUseCase,
)


@pytest.fixture
def domain_repository(db_in_memory) -> DomainRepository:
    return DomainRepository(db_in_memory)


@pytest.fixture
def new_ct_event_use_case(postgres_config):
    return NewCtEventUseCase(None, postgres_config)


@pytest.fixture
def subscribe_new_domains_use_case(facebook_config, postgres_config):
    return SubscribeNewDomainsUseCase(facebook_config, postgres_config)
