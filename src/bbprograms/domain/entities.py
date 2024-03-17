import pydantic
import typing

from core.arch import Entity

from .exceptions import (
    InvalidAssetTypeException,
    InvalidPlatformException,
)


PLATFORMS = [
    'bugcrowd',
    'bizone',
    'hackerone'
]

ASSET_TYPES = [
    'other',
    'domain',
    'wildcard_domain',
    'host',
    'subnet',
    'mobile'
]


class AssetEntity(Entity):
    type: str
    value: str
    is_paid: bool

    @pydantic.field_validator('type')
    def type_validator(cls, v):
        if v not in ASSET_TYPES:
            raise InvalidAssetTypeException

        return v


class BugBountyProgramEntity(Entity):
    program_name: str
    program_site: str
    platform: str

    in_scope: typing.List[AssetEntity]
    out_of_scope: typing.List[AssetEntity]

    notes: str

    @pydantic.field_validator('platform')
    def platform_validator(cls, v):
        if v not in PLATFORMS:
            raise InvalidPlatformException

        return v
