from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.bugbounty_programs.api import Asset, ProgramData, Program
from asman.domains.bugbounty_programs.repo import ProgramRepository


class UpdateProgramUseCase(AbstractUseCase):
    def __init__(self, config: BaseSettings, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.repo = ProgramRepository(database)

    async def execute(self, program: Program) -> Program | None:
        updated_program = await self.repo.update(program)

        return updated_program
