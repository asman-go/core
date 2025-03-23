from pydantic_settings import BaseSettings
from typing import Sequence

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import AssetId, ProgramId
from asman.domains.bugbounty_programs.repo import AssetRepository
from asman.domains.bugbounty_programs.domain import TABLE_ASSET_NAME


class RemoveAssetsUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = AssetRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_ASSET_NAME,
        )

    async def execute(self, request: AssetId | ProgramId) -> Sequence[AssetId]:
        # Можем удалить по asset id или по program id
        return await self.repo.delete([request])
