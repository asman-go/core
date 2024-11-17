import pytest

from asman.domains.facebook_api.use_cases import (
    NewCtEventUseCase,
    SubscribeNewDomainsUseCase,
)


# TODO: подумать, как написать тест для Facebook API


def test_subscribe_new_domains_use_case_create(facebook_config):
    use_case = SubscribeNewDomainsUseCase(facebook_config, None)

    assert use_case, 'Use case is not created'
    assert use_case.config, 'Config property not found'
    assert use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_subscribe_new_domains_use_case_execute(
            subscribe_new_domains_use_case: SubscribeNewDomainsUseCase
        ):
    # TBD
    domains = ['example.com', 'test.com']
    
    ...
