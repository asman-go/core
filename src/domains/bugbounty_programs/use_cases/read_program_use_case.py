from pydantic_settings import BaseSettings
from typing import Iterable, Sequence

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.bugbounty_programs.api import Asset, ProgramData, ProgramId, Program
from asman.domains.bugbounty_programs.repo import ProgramRepository


class ReadProgramUseCase(AbstractUseCase):
    def __init__(self, config: BaseSettings, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.repo = ProgramRepository(database)

    async def execute(self) -> Sequence[Program]:
        programs = await self.repo.list()

        return programs


class ReadProgramByIdUseCase(AbstractUseCase):
    def __init__(self, config: BaseSettings, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.repo = ProgramRepository(database)

    async def execute(self, programId: ProgramId) -> Program | None:
        program = await self.repo.get_by_id(programId)

        return program
