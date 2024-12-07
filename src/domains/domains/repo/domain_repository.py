from typing import Sequence, Dict, List

from sqlalchemy import select, update, delete, insert
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.orm import Session

from asman.core.adapters.db import Database, Postgres
from asman.core.arch import AbstractRepository, Entity
from asman.core.exceptions import NotImplementedException

from asman.domains.domains.domain import (
    TableDomain,
)

class DomainRepository(AbstractRepository):
    def __init__(self, database: Postgres) -> None:
        self.database = database

    async def insert(self, entities: Dict[str, List[str]]) -> None:

        with Session(self.database.engine) as session:
            domains = list()
            for parent_domain in entities:
                domains.extend(
                    map(
                        lambda domain: {
                            'domain': domain,
                            'parent_domain': parent_domain,
                        },
                        # TableDomain(
                        #     domain=domain,
                        #     parent_domain=parent_domain
                        # ),
                        entities[parent_domain]
                    )
                )
            stmt = (
                postgres_insert(TableDomain)
                .values(domains)
                # Чтобы использовать эту функцию, надо использовать insert из диалекта postgres, а не общую
                .on_conflict_do_nothing()
            )
            session.execute(stmt)
            # session.add_all(domains)
            session.commit()

    async def update(self, entity: Entity) -> Entity:
        raise NotImplementedException

    async def get_by_id(self, entity_id) -> Entity | None:
        raise NotImplementedException

    async def list(self, parent_domain: str) -> Sequence[str] | None:
        with Session(self.database.engine) as session:
            rows = (
                session.query(TableDomain)
                .filter_by(parent_domain=parent_domain)
                .all()
            )
            return list(
                map(
                    lambda x: x.domain,
                    rows
                )
            )

    async def delete(self, parent_domain: str):
        with Session(self.database.engine) as session:
            stmt = (
                delete(TableDomain)
                .where(TableDomain.parent_domain == parent_domain)
            )
            session.execute(stmt)
            session.commit()
