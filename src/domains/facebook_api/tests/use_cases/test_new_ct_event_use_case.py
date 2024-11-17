import pytest

from asman.domains.facebook_api.use_cases import (
    NewCtEventUseCase,
    SubscribeNewDomainsUseCase,
)
from asman.domains.facebook_api.api import (
    FacebookCtEvent,
    NewCertificateEvent,
    FACEBOOK_EVENT,
)


def test_new_ct_event_use_case_create():
    use_case = NewCtEventUseCase(None, None)

    assert use_case, 'Use case is not created'
    assert use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_new_ct_event_use_case_execute(
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
