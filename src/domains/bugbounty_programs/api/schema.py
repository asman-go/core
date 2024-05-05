from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from pydantic import (
    PositiveInt,
    StrictBool,
    StrictStr,
)


class AssetType(Enum):
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


class ProgramData(BaseModel):
    program_name: StrictStr
    program_site: StrictStr
    platform: StrictStr
    assets: List[Asset]
    notes: StrictStr


class ProgramId(BaseModel):
    id: PositiveInt


class Program(BaseModel):
    id: ProgramId
    data: ProgramData
