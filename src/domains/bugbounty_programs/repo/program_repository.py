from pydantic import BaseModel, Field
from typing import Sequence

from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import AbstractRepository, Entity
from asman.core.exceptions import NotImplementedException

from asman.domains.bugbounty_programs.domain import (
    TableAsset,
    TableProgram,
    TABLE_ASSET_NAME,
    TABLE_BUGBOUNTY_PROGRAM_NAME,
)

from asman.domains.bugbounty_programs.api import (
    # CreateProgramRequest,
    Program,
    ProgramData,
)


class _Search(BaseModel):
    id: str = Field()


class _SearchByProgram(BaseModel):
    program_id: str = Field()


class ProgramRepository(AbstractRepository):
    def __init__(self, database: DatabaseFacade) -> None:
        self.database = database

    async def insert(self, entity: ProgramData) -> int | None:
        # И здесь вероятно будут проблемы
        self.database.upsert(entity.assets, TABLE_ASSET_NAME)
        self.database.upsert([entity], TABLE_BUGBOUNTY_PROGRAM_NAME)

        return -1
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
        # Здесь вероятно будут проблемы
        self.database.upsert([entity], TABLE_BUGBOUNTY_PROGRAM_NAME)
        found = self.database.query([_Search(id=entity.id)], TABLE_BUGBOUNTY_PROGRAM_NAME)
        assert found
        assert len(found) == 1

        return TableProgram.convert(found[0])

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
        found = self.database.query([_Search(id=entity_id)], TABLE_BUGBOUNTY_PROGRAM_NAME)

        if found and len(found) == 1:
            return TableProgram.convert(found[0])

        return None

    async def list(self) -> Sequence[Program] | None:
        found = self.database.query(table_name=TABLE_BUGBOUNTY_PROGRAM_NAME)

        return list(
            map(
                lambda x: TableProgram.convert(x),
                found
            )
        )

    async def delete(self, program_id: int):
        # TODO: transaction
        self.database.delete([_SearchByProgram(program_id=program_id)], TABLE_ASSET_NAME)
        self.database.delete([_Search(id=program_id)], TABLE_BUGBOUNTY_PROGRAM_NAME)
