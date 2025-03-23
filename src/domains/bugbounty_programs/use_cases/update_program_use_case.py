from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import Asset, NewProgram, Program
from asman.domains.bugbounty_programs.repo import ProgramRepository
from asman.domains.bugbounty_programs.domain import TABLE_BUGBOUNTY_PROGRAM_NAME


class UpdateProgramUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = ProgramRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_BUGBOUNTY_PROGRAM_NAME,
        )

    async def execute(self, program: Program) -> Program | None:
        updated_program = await self.repo.update(program)

        return updated_program
