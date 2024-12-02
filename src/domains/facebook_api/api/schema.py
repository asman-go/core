from pydantic import BaseModel, field_validator, Field
from pydantic import (
    PositiveInt,
    StrictStr,
)

from typing import List, Dict, Optional, Mapping

from .exceptions import WrongEventTypeException
from .pem import get_domains_from_certificate


FACEBOOK_EVENT = 'certificate_transparency'


class ChangesField(BaseModel):
    field: StrictStr
    value: Mapping
    # value: Dict[str, str] = Field(default_factory=lambda: dict())

    @field_validator('value')
    def changes_validator(cls, value):
        # print('changes_validator', value)
        d = dict()
        if 'certificate_pem' in value:
            parent_domain, domains = get_domains_from_certificate(
                value['certificate_pem']
            )

            d[parent_domain] = domains
        return d


class NewCertificateEvent(BaseModel):
    id: StrictStr
    changes: List[ChangesField] = Field(default_factory=lambda: list())
    # changed_fields: List[StrictStr] = Field(default_factory=lambda: list())
    # changes: Dict[str, Mapping] = Field(default_factory=lambda: dict())  # Dict[str, List[str]]
    time: PositiveInt

    # @field_validator('changed_fields')
    # def changed_fields_validator(cls, value):
    #     if 'certificate' in value:
    #         # I don't know how to do that
    #         # I need to get information about certificate with id
    #         # ??? SubscribeNewDomainsUseCase ???
    #         ...

    #     return value



class FacebookCtEvent(BaseModel):
    """
        certificate_transparency event:
            https://developers.facebook.com/docs/certificate-transparency/certificates-webhook#certificate-alert-webhook
    """
    object: StrictStr
    entry: List[NewCertificateEvent]

    @field_validator('object')
    def object_validator(cls, value):
        if value != FACEBOOK_EVENT:
            raise WrongEventTypeException

        return value
