import pytest

from asman.domains.services.use_cases.archive import (
    UnsubscribeDomainsUseCase,
)


# TODO: подумать, как написать тест для Facebook API


@pytest.mark.asyncio
async def _test_unsubscribe_domains_use_case_execute(
            unsubscribe_domains_use_case: UnsubscribeDomainsUseCase
        ):
    # TBD
    domains = ['example.com', 'test.com']
    
    ...
