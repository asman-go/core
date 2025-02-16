from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import AddAssetsRequest
from asman.domains.bugbounty_programs.repo import AssetRepository


class AddAssetsUseCase(AbstractUseCase):
    def __init__(self) -> None:
        database = DatabaseFacade(Databases.PostgreSQL)
        self.repo = AssetRepository(database)

    async def execute(self, request: AddAssetsRequest):
        await self.repo.insert(request.program_id, request.assets)
