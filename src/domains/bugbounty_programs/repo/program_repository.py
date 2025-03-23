from pydantic import BaseModel
from typing import Sequence

from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import AbstractRepository

from asman.domains.bugbounty_programs.api import (
    ProgramId,
    Program,
    NewProgram,
)
from asman.domains.bugbounty_programs.domain import TableProgram


class ProgramRepository(AbstractRepository):
    def __init__(self, database: DatabaseFacade, table_name: str) -> None:
        self.database = database
        self.table_name = table_name

    async def insert(self, entities: Sequence[NewProgram]) -> Sequence[ProgramId]:
        ids = self.database.upsert(self.table_name, entities)

        return list(
            map(
                lambda id: ProgramId(program_id=id[0]),
                ids,
            )
        )

    async def update(self, entities: Sequence[Program]) -> Sequence[ProgramId]:
        ids =  self.database.upsert(self.table_name, entities)

        return list(
            map(
                lambda id: ProgramId(program_id=id[0]),
                ids,
            )
        )

    async def search(self, filter: Sequence[BaseModel]) -> Sequence[Program]:
        return list(
            map(
                lambda program: TableProgram.convert(program),
                self.database.query(self.table_name, filter),
            )
        )

    async def list(self) -> Sequence[Program]:
        return list(
            map(
                lambda program: TableProgram.convert(program),
                self.database.query(self.table_name),
            )
        )

    async def delete(self, filter: Sequence[BaseModel]) -> Sequence[ProgramId]:
        ids = self.database.delete(self.table_name, filter)
        return list(
            map(
                lambda id: ProgramId(program_id=id[0]),
                ids,
            )
        )
