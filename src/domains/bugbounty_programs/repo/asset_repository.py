from pydantic import BaseModel
from typing import Sequence

from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import AbstractRepository
from asman.core.exceptions import NotImplementedException

from asman.domains.bugbounty_programs.domain import TableAsset, TABLE_ASSET_NAME
from asman.domains.bugbounty_programs.api import NewLinkedAsset, LinkedAsset, Asset, AssetId


class AssetRepository(AbstractRepository):
    def __init__(self, database: DatabaseFacade, table_name: str) -> None:
        self.database = database
        self.table_name = table_name

    async def insert(self, entities: Sequence[NewLinkedAsset]) -> Sequence[AssetId]:
        ids = self.database.upsert(self.table_name, entities)

        return list(
            map(
                lambda id: AssetId(id=id[0]),
                ids,
            )
        )

    async def update(self, entities: Sequence[LinkedAsset]) -> Sequence[AssetId]:
        ids = self.database.upsert(self.table_name, entities)
        return list(
            map(
                lambda id: AssetId(id=id[0]),
                ids,
            )
        )

    async def search(self, filter: Sequence[BaseModel]) -> Sequence[Asset]:
        return list(
            map(
                lambda asset: TableAsset.convert(asset),
                self.database.query(self.table_name, filter),
            )
        )

    async def list(self) -> Sequence[Asset]:
        return list(
            map(
                lambda asset: TableAsset.convert(asset),
                self.database.query(self.table_name),
            )
        )

    async def delete(self, filter: Sequence[AssetId]):
        ids = self.database.delete(self.table_name, filter)

        return list(
            map(
                lambda id: AssetId(id=id[0]),
                ids,
            )
        )
