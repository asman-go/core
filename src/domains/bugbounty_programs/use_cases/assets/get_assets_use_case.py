from typing import Sequence

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import ProgramId, Asset
from asman.domains.bugbounty_programs.repo import AssetRepository
from asman.domains.bugbounty_programs.domain import TABLE_ASSET_NAME


class GetAssetsUseCase(AbstractUseCase):
    def __init__(self):
        self.repo = AssetRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_ASSET_NAME,
        )

    async def execute(self, request: ProgramId) -> Sequence[Asset]:
        return await self.repo.search([request])
