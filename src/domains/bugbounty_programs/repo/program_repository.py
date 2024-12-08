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
    # CreateProgramRequest,
    Program,
    ProgramData,
)


class ProgramRepository(AbstractRepository):
    def __init__(self, database: Postgres) -> None:
        self.database = database

    async def insert(self, entity: ProgramData) -> int | None:
        # Use a transaction
        with Session(self.database.engine) as session:
            # Ищем, вдруг такая программа уже есть
            programs = await self.list()
            programs = list(filter(lambda program: program.data == entity, programs))
            if programs:
                return programs[0].id

            # Добавляем программу
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
                        type=asset.type.value,
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

    async def update(self, entity: Program) -> Program:
        """
            ассеты нельзя обновить, можно добавить или удалить
        """
        with Session(self.database.engine) as session:
            stmt = (
                update(TableProgram)
                .where(TableProgram.id == entity.id)
                .values(
                    program_name=entity.data.program_name,
                    program_site=entity.data.program_site,
                    platform=entity.data.platform,
                    notes=entity.data.notes,
                )
            )
            session.execute(stmt)
            session.commit()

            updated_entity = (
                session.query(TableProgram)
                .filter_by(
                    id=entity.id,
                )
                .first()
            )

            return TableProgram.convert(updated_entity)

    async def get_by_id(self, entity_id: int) -> Program | None:
        with Session(self.database.engine) as session:
            # row = session.scalar(
            #     select(TableProgram)
            #     .where(TableProgram.id == entity_id)
            # )
            row = (
                session.query(TableProgram)
                .filter_by(id=entity_id)
                .first()
            )

            return TableProgram.convert(row) if row else None

    async def list(self) -> Sequence[Program] | None:
        with Session(self.database.engine) as session:
            rows = (
                session.query(TableProgram)
                .all()
            )
            return list(
                map(
                    lambda x: TableProgram.convert(x),
                    rows
                )
            )

    async def delete(self, program_id: int):
        with Session(self.database.engine) as session:
            stmt = (
                delete(TableAsset)
                .where(TableAsset.program_id == program_id)
            )
            session.execute(stmt)

            stmt = (
                delete(TableProgram)
                .where(TableProgram.id == program_id)
            )
            session.execute(stmt)

            session.commit()
