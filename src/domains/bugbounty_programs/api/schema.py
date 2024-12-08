from enum import Enum, IntEnum
from typing import List
from pydantic import BaseModel, Field
from pydantic import (
    PositiveInt,
    StrictBool,
    StrictStr,
)


class AssetType(IntEnum):
    ASSET_MOBILE = 0
    ASSET_WEB = 1
    ASSET_API = 2
    ASSET_IP = 3
    ASSET_SUBNET = 4

    ASSET_OTHER = 9999
    ASSET_UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return AssetType.ASSET_UNKNOWN


class Asset(BaseModel):
    value: StrictStr
    type: AssetType
    in_scope: StrictBool
    is_paid: StrictBool

    def __eq__(self, other: 'Asset'):
        return (
            self.value == other.value
            and self.type.value == other.type.value
        )

    def __str__(self):
        return f'{self.type.name}:{self.value}'

    def __hash__(self):
        return hash(str(self))


class ProgramData(BaseModel):
    program_name: StrictStr
    program_site: StrictStr
    platform: StrictStr
    assets: List[Asset]
    notes: StrictStr

    def __eq__(self, other: 'ProgramData'):
        return (
            self.program_site == other.program_site
            and self.program_name == other.program_name
            and self.platform == other.platform
        )


class Program(BaseModel):
    id: PositiveInt
    data: ProgramData

    def __eq__(self, other: 'Program'):
        return self.data == other.data


class AddAssetsRequest(BaseModel):
    program_id: PositiveInt
    assets: List[Asset]


class RemoveAssetsRequest(BaseModel):
    program_id: PositiveInt
    assets: List[Asset]
