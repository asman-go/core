from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.bugbounty_programs.api import RemoveAssetsRequest
from asman.domains.bugbounty_programs.repo import AssetRepository


class RemoveAssetsUseCase(AbstractUseCase):
    def __init__(self, config: BaseSettings, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.repo = AssetRepository(database)

    async def execute(self, request):
        await self.repo.delete(request.program_id, request.assets)
