import pytest

from asman.domains.services.use_cases.archive import (
    NewCtEventUseCase,
    SubscribeNewDomainsUseCase,
)


# TODO: подумать, как написать тест для Facebook API


@pytest.mark.asyncio
async def _test_subscribe_new_domains_use_case_execute(
            subscribe_new_domains_use_case: SubscribeNewDomainsUseCase
        ):
    # TBD
    domains = ['example.com', 'test.com']
    
    ...
