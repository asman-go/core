import pytest

from asman.domains.domains.use_cases import (
    UnsubscribeDomainsUseCase,
)


# TODO: подумать, как написать тест для Facebook API


def test_unsubscribe_domains_use_case_create(facebook_config):
    use_case = UnsubscribeDomainsUseCase(facebook_config, None)

    assert use_case, 'Use case is not created'
    assert use_case.config, 'Config property not found'
    assert use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_unsubscribe_domains_use_case_execute(
            unsubscribe_domains_use_case: UnsubscribeDomainsUseCase
        ):
    # TBD
    domains = ['example.com', 'test.com']
    
    ...
