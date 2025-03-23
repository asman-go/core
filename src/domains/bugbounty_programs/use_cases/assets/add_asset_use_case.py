from pydantic_settings import BaseSettings
from typing import Sequence

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import AddAssetsRequest, AssetId, NewLinkedAsset
from asman.domains.bugbounty_programs.repo import AssetRepository

from asman.domains.bugbounty_programs.domain import TABLE_ASSET_NAME


class AddAssetsUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = AssetRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_ASSET_NAME,
        )

    async def execute(self, request: AddAssetsRequest) -> Sequence[AssetId]:
        assets = list(map(
            lambda new_asset: NewLinkedAsset(
                program_id=request.program_id,
                **new_asset.model_dump(),
            ),
            request.assets,
        ))
        return await self.repo.insert(assets)
