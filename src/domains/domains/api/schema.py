from pydantic import BaseModel, field_validator, Field
from pydantic import (
    PositiveInt,
    StrictStr,
)
import re

from typing import List, Mapping

from .exceptions import WrongEventTypeException, IncorrectDomainException
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


class Domain(BaseModel):
    domain: str
    parent_domain: str

    @field_validator('domain', 'parent_domain')
    def domain_validator(cls, value: str):
        _value = value
        if _value[:2] == '*.':
            _value = _value[2:]

        if _value[0] == '.':
            _value = _value[1:]

        parts = _value.split('.')
        for part in parts[:-1]:
            if not bool(re.match(r'^[A-Za-z0-9-]{1,63}$', part)):
                raise IncorrectDomainException

        # check TLD
        if not bool(re.match(r'^[A-Za-z]{2,}$', parts[-1])):
            raise IncorrectDomainException

        return _value

    def __eq__(self, other: 'Domain'):
        return (
            self.domain == other.domain
            and self.parent_domain == other.parent_domain
        )

    def __str__(self):
        return f'{self.parent_domain}:{self.domain}'

    def __hash__(self):
        return hash(str(self))


class SearchByParentDomain(BaseModel):
    parent_domain: str


class SearchByDomain(BaseModel):
    domain: str
