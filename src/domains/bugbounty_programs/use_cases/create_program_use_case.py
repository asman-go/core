from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import NewProgram
from asman.domains.bugbounty_programs.repo import ProgramRepository
from asman.domains.bugbounty_programs.domain import TABLE_BUGBOUNTY_PROGRAM_NAME


class CreateProgramUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = ProgramRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_BUGBOUNTY_PROGRAM_NAME,
        )

    async def execute(self, request: NewProgram) -> int:
        program_id = await self.repo.insert(request)
        return program_id
