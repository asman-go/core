from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.bugbounty_programs.repo import ProgramRepository


class DeleteProgramUseCase(AbstractUseCase):
    def __init__(self, config: BaseSettings, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.repo = ProgramRepository(database)

    async def execute(self, program_id: int) -> bool:
        await self.repo.delete(program_id)

        return True
