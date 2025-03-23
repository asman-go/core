from pydantic_settings import BaseSettings
from typing import Iterable, Sequence

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import Asset, NewProgram, Program
from asman.domains.bugbounty_programs.repo import ProgramRepository
from asman.domains.bugbounty_programs.domain import TABLE_BUGBOUNTY_PROGRAM_NAME


class ReadProgramUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = ProgramRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_BUGBOUNTY_PROGRAM_NAME,
        )

    async def execute(self) -> Sequence[Program]:
        programs = await self.repo.list()

        return programs


class ReadProgramByIdUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = ProgramRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_BUGBOUNTY_PROGRAM_NAME,
        )

    async def execute(self, program_id: int) -> Program | None:
        program = await self.repo.get_by_id(program_id)

        return program
