from pydantic import BaseModel, field_validator
from pydantic import (
    PositiveInt,
    StrictStr,
)

from typing import List, Dict, Optional

from .exceptions import WrongEventTypeException
from .pem import get_domains_from_certificate


class NewCertificateEvent(BaseModel):
    id: StrictStr
    changed_fields: List[StrictStr]
    changes: Dict[str, List[str]]
    time: PositiveInt

    @field_validator('changed_fields')
    def changed_fields_validator(cls, value):
        if 'certificate' in value:
            # I don't know how to do that
            # I need to get information about certificate with id
            # ??? SubscribeNewDomainsUseCase ???
            ...

        return value

    @field_validator('changes')
    def changes_validator(cls, value):
        print('changes_validator', value)
        d = dict()
        if 'value' in value and 'certificate_pem' in value['value']:
            parent_domain, domains = get_domains_from_certificate(
                value['value']['certificate_pem']
            )

            d[parent_domain] = domains
        return d


class FacebookCtEvent(BaseModel):
    """
        certificate_transparency event:
            https://developers.facebook.com/docs/certificate-transparency/certificates-webhook#certificate-alert-webhook
    """
    object: StrictStr
    entry: List[NewCertificateEvent]

    @field_validator('object')
    def object_validator(cls, value):
        FACEBOOK_EVENT = 'certificate_transparency'
        if value != FACEBOOK_EVENT:
            raise WrongEventTypeException

        return value
