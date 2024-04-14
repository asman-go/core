from pydantic_settings import BaseSettings

from asman.core.arch import AbstractUseCase
from asman.core.adapters.db import Postgres, PostgresConfig

from asman.domains.bugbounty_programs.api import CreateProgramRequest
from asman.domains.bugbounty_programs.repo import ProgramRepository


class CreateProgramUseCase(AbstractUseCase):
    def __init__(self, config: BaseSettings, databaseConfig: PostgresConfig, *argv) -> None:
        database = Postgres(databaseConfig)
        self.repo = ProgramRepository(database)

    async def execute(self, request: CreateProgramRequest) -> int:
        program_id = await self.repo.insert(request)
        return program_id
