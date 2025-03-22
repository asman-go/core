from pydantic import BaseModel, Field, create_model
from typing import Sequence

from sqlalchemy import select, insert, update, delete, and_
from sqlalchemy.orm import Session

from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import AbstractRepository, Entity
from asman.core.exceptions import NotImplementedException

from asman.domains.bugbounty_programs.domain import (
    TableAsset,
    TableProgram,
)
from asman.domains.bugbounty_programs.domain import (
    TABLE_ASSET_NAME,
    TABLE_BUGBOUNTY_PROGRAM_NAME,
)

from asman.domains.bugbounty_programs.api import (
    # CreateProgramRequest,
    Asset,
    Program,
    ProgramData,
)

from .utils import SearchById, SearchByProgramId


class AssetRepository(AbstractRepository):
    def __init__(self, database: DatabaseFacade) -> None:
        self.database = database

    async def insert(self, program_id: int, entities: Sequence[Asset]) -> None:

        _assets = self.database.query(
            query=[SearchByProgramId(program_id=program_id)],
            table_name=TABLE_ASSET_NAME,
        )
        with Session(self.database.engine) as session:
            program = (
                session.query(TableProgram)
                .filter_by(
                    id=program_id,
                )
                .first()
            )

            # Добавляем только новые ассеты
            program_model = TableProgram.convert(program) if program else None
            new_entities = list(
                filter(lambda asset: asset not in program_model.data.assets, entities)
            )

            assets = list(
                map(
                    lambda asset: TableAsset(
                        program=program,

                        value=asset.value,
                        type=asset.type.value,
                        in_scope=asset.in_scope,
                        is_paid=asset.is_paid,
                    ),
                    new_entities
                )
            )

            session.add_all(assets)
            session.commit()

    async def update(self, entity: Entity) -> Entity:
        """
            ассеты нельзя обновить, можно добавить или удалить
        """
        raise NotImplementedException

    async def get_by_id(self, entity_id) -> Entity | None:
        raise NotImplementedException

    async def list(self, program_id: int) -> Sequence[Asset] | None:
        found = self.database.query([SearchByProgramId(program_id=program_id)])
        if not found:
            return None
        
        return list(
                map(
                    lambda x: TableAsset.convert(x),
                    found
                )
            )
        with Session(self.database.engine) as session:
            rows = (
                session.query(TableAsset)
                .filter_by(program_id=program_id)
                .all()
            )
            # rows = session.execute(
            #     select(TableAsset)
            #     .where(program_id=program_id)
            # )
            return list(
                map(
                    lambda x: TableAsset.convert(x),
                    rows
                )
            )

    async def delete(self, program_id: int, entities: Sequence[Asset]) -> None:
        with Session(self.database.engine) as session:
            stmt = (
                delete(TableAsset)
                .where(
                    and_(
                        TableAsset.program_id == program_id,
                        TableAsset.value.in_(
                            list(map(
                                lambda x: x.value,
                                entities
                            ))
                        ),
                    )
                )
            )
            session.execute(stmt)
            session.commit()
