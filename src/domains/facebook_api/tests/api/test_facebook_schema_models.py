import pytest
import pydantic

from asman.domains.facebook_api.api.exceptions import WrongEventTypeException
from asman.domains.facebook_api.api.schema import (
    NewCertificateEvent,
    FacebookCtEvent,
    FACEBOOK_EVENT,
)


def test_new_certificate_event_entity_create(new_certificate_event_json):
    entity = pydantic.TypeAdapter(
        NewCertificateEvent
    ).validate_python(
        new_certificate_event_json
    )

    assert entity
    assert entity.id == new_certificate_event_json['id']
    assert entity.time == new_certificate_event_json['time']
    assert entity.changed_fields == new_certificate_event_json['changed_fields']
    assert '*.example.company' in entity.changes
    assert entity.changes['*.example.company'] == ['example.com', 'www.example.com', 'mail.example.com', 'ftp.example.com']


def test_facebook_ct_event_entity_create(new_certificate_event_json):
    entity = pydantic.TypeAdapter(
        FacebookCtEvent
    ).validate_python({
        'object': FACEBOOK_EVENT,
        'entry': [
            NewCertificateEvent(**new_certificate_event_json),
        ],
    })

    assert entity
    assert entity.object == FACEBOOK_EVENT
    assert len(entity.entry) == 1


def test_facebook_ct_event_entity_create_throws_exception():
    with pytest.raises(WrongEventTypeException) as exc:
        FacebookCtEvent(
            object='notexisted',
            entry=[],
        )

    assert isinstance(exc.value, WrongEventTypeException)