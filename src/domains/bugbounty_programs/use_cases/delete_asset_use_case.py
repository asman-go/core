from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import RemoveAssetsRequest
from asman.domains.bugbounty_programs.repo import AssetRepository
from asman.domains.bugbounty_programs.domain import TABLE_ASSET_NAME


class RemoveAssetsUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = AssetRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_ASSET_NAME,
        )

    async def execute(self, request: RemoveAssetsRequest):
        await self.repo.delete(request.program_id, request.assets)
