from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import AddAssetsRequest
from asman.domains.bugbounty_programs.repo import AssetRepository

from asman.domains.bugbounty_programs.domain import TABLE_ASSET_NAME


class AddAssetsUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = AssetRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_ASSET_NAME,
        )

    async def execute(self, request: AddAssetsRequest):
        await self.repo.insert(request.program_id, request.assets)
