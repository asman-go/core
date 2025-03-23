from pydantic import BaseModel
from typing import Sequence

from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import AbstractRepository
from asman.core.exceptions import NotImplementedException

from asman.domains.bugbounty_programs.domain import TableAsset, TABLE_ASSET_NAME
from asman.domains.bugbounty_programs.api import LinkedAsset, Asset


class AssetRepository(AbstractRepository):
    def __init__(self, database: DatabaseFacade) -> None:
        self.database = database

    async def insert(self, entities: Sequence[LinkedAsset]) -> Sequence[Asset]:
        raise NotImplementedException

    async def update(self, entities: Sequence[LinkedAsset]) -> Sequence[Asset]:
        ids = self.database.upsert(TABLE_ASSET_NAME, entities)
        return self.database.query(TABLE_ASSET_NAME, ids)

    async def search(self, filter: Sequence[BaseModel]) -> Sequence[BaseModel]:
        raise NotImplementedException

    async def list(self) -> Sequence[BaseModel]:
        raise NotImplementedException

    async def delete(self, filter: Sequence[BaseModel]):
        raise NotImplementedException
