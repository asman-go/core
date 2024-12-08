from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.bugbounty_programs.api import AddAssetsRequest
from asman.domains.bugbounty_programs.repo import AssetRepository


class AddAssetsUseCase(AbstractUseCase):
    def __init__(self, config: BaseSettings, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.repo = AssetRepository(database)

    async def execute(self, request: AddAssetsRequest):
        await self.repo.insert(request.program_id, request.assets)
