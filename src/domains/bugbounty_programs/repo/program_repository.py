from typing import Sequence

from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

from asman.core.adapters.db import Postgres
from asman.core.arch import AbstractRepository, Entity
from asman.core.exceptions import NotImplementedException

from asman.domains.bugbounty_programs.domain import (
    TableAsset,
    TableProgram,
)

from asman.domains.bugbounty_programs.api import (
    CreateProgramRequest,
)


class ProgramRepository(AbstractRepository):
    def __init__(self, database: Postgres) -> None:
        self.database = database

    async def insert(self, entity: CreateProgramRequest) -> int | None:
        # Use a transaction
        with Session(self.database.engine) as session:
            NEW_PROGRAM = TableProgram(
                program_name = entity.program_name,
                program_site = entity.program_site,
                platform = entity.platform,
                notes = entity.notes,
            )
            session.add(NEW_PROGRAM)

            assets = list(
                map(
                    lambda asset: TableAsset(
                        program=NEW_PROGRAM,

                        value=asset.value,
                        type=asset.type,
                        in_scope=asset.in_scope,
                        is_paid=asset.is_paid,
                    ),
                    entity.assets
                )
            )

            session.add_all(assets)

            session.commit()

            # return session.scalars(
            #     select(TableProgram)
            #     .where(TableProgram.platform == entity.platform)
            #     .where(TableProgram.program_site == entity.program_site)
            # ).one().id

            return NEW_PROGRAM.id

    def update(self, entity: Entity) -> Entity:
        raise NotImplementedException

    def get_by_id(self, entity_id) -> Entity | None:
        raise NotImplementedException

    def list(self) -> Sequence[Entity] | None:
        raise NotImplementedException

    def delete(self, entity_id):
        raise NotImplementedException
