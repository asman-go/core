import pytest

from asman.domains.domains.use_cases import (
    NewCtEventUseCase,
    SubscribeNewDomainsUseCase,
)
from asman.domains.domains.api import (
    FacebookCtEvent,
    NewCertificateEvent,
    FACEBOOK_EVENT,
)


@pytest.mark.asyncio
async def _test_new_ct_event_use_case_execute(
            new_ct_event_use_case: NewCtEventUseCase,
            new_certificate_event: NewCertificateEvent,
        ):

    event = FacebookCtEvent(
        object=FACEBOOK_EVENT,
        entry=[
            new_certificate_event,
        ]
    )
    status = await new_ct_event_use_case.execute(event)

    assert status
