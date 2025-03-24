from pydantic_settings import BaseSettings
from typing import Iterable, Sequence

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import DatabaseFacade, Databases

from asman.domains.bugbounty_programs.api import ProgramNotFound, Program, SearchByID
from asman.domains.bugbounty_programs.repo import ProgramRepository
from asman.domains.bugbounty_programs.domain import TABLE_BUGBOUNTY_PROGRAM_NAME


class ReadProgramUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = ProgramRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_BUGBOUNTY_PROGRAM_NAME,
        )

    async def execute(self) -> Sequence[Program]:
        return await self.repo.list()


class ReadProgramByIdUseCase(AbstractUseCase):
    def __init__(self) -> None:
        self.repo = ProgramRepository(
            DatabaseFacade(Databases.PostgreSQL),
            TABLE_BUGBOUNTY_PROGRAM_NAME,
        )

    async def execute(self, request: SearchByID) -> Program:
        programs = await self.repo.search([request])

        if not programs:
            raise ProgramNotFound('ReadProgramByIdUseCase: программа не обнаружена')

        return programs[0]
