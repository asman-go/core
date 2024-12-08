from pydantic_settings import BaseSettings
from typing import Iterable, Sequence

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.bugbounty_programs.api import Asset, ProgramData, Program
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

    async def execute(self, program_id: int) -> Program | None:
        program = await self.repo.get_by_id(program_id)

        return program
