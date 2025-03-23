from enum import Enum, IntEnum
from typing import List
from pydantic import BaseModel, Field
from pydantic import (
    PositiveInt,
    StrictBool,
    StrictStr,
)


class ProgramId(BaseModel):
    program_id: PositiveInt


class AssetId(BaseModel):
    id: PositiveInt


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


class NewAsset(BaseModel):
    value: StrictStr
    type: AssetType
    in_scope: StrictBool
    is_paid: StrictBool

    def __eq__(self, other: 'NewAsset'):
        return (
            self.value == other.value
            and self.type.value == other.type.value
        )

    def __str__(self):
        return f'{self.type.name}:{self.value}'

    def __hash__(self):
        return hash(str(self))


class NewLinkedAsset(NewAsset):
    program_id: PositiveInt


class Asset(NewAsset):
    id: PositiveInt


class LinkedAsset(Asset):
    program_id: PositiveInt


class NewProgram(BaseModel):
    program_name: StrictStr
    program_site: StrictStr
    platform: StrictStr
    notes: StrictStr

    def __eq__(self, other: 'NewProgram'):
        return (
            self.program_site == other.program_site
            and self.program_name == other.program_name
            and self.platform == other.platform
        )


class Program(NewProgram):
    id: PositiveInt


class SearchByID(BaseModel):
    id: PositiveInt


class AddAssetsRequest(ProgramId):
    assets: List[NewAsset]


class RemoveAssetsRequest(ProgramId):
    assets: List[NewAsset]
