import pytest

from asman.core.adapters.tests import facebook_config
from asman.domains.services.use_cases.archive import (
    NewCtEventUseCase,
    SubscribeNewDomainsUseCase,
    UnsubscribeDomainsUseCase,
)


@pytest.fixture
def new_ct_event_use_case():
    return NewCtEventUseCase()


@pytest.fixture
def subscribe_new_domains_use_case(facebook_config):
    return SubscribeNewDomainsUseCase(facebook_config)


@pytest.fixture
def unsubscribe_domains_use_case(facebook_config):
    return UnsubscribeDomainsUseCase(facebook_config)
