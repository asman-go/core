from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import ProgramId, SearchByID
from asman.domains.bugbounty_programs.repo import ProgramRepository, AssetRepository
from asman.domains.bugbounty_programs.domain import TABLE_BUGBOUNTY_PROGRAM_NAME, TABLE_ASSET_NAME


class DeleteProgramUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo_assets = AssetRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_ASSET_NAME,
        )
        self.repo_programs = ProgramRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_BUGBOUNTY_PROGRAM_NAME,
        )

    async def execute(self, request: SearchByID) -> ProgramId:
        # TODO: transactions
        await self.repo_assets.delete([ProgramId(program_id=request.id)])
        ids = await self.repo_programs.delete([request])

        return ids[0]
