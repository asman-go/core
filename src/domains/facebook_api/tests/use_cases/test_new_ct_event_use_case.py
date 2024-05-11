import pytest

from asman.domains.facebook_api.use_cases import (
    NewCtEventUseCase,
    SubscribeNewDomainsUseCase,
)
from asman.domains.facebook_api.api import (
    FacebookCtEvent,
    NewCertificateEvent,
)


def test_new_ct_event_use_case_create():
    use_case = NewCtEventUseCase(None, None)

    assert use_case, 'Use case is not created'
    assert use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_new_ct_event_use_case_execute(
            new_ct_event_use_case: NewCtEventUseCase
        ):
    # TODO: make good tests
    event = FacebookCtEvent(
        object='certificate_transparency',
        entry=[
            NewCertificateEvent(
                id='test',
                changed_fields=[],
                changes={
                    'value': {
                        'certificate_pem': 'TBD'
                    }
                },
                time=123124,
            )
        ]
    )
    # await new_ct_event_use_case.execute(event)
    ...
