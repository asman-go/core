from typing import Sequence, Dict, List
from pydantic import BaseModel

from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import AbstractRepository
from asman.core.exceptions import NotImplementedException

from asman.domains.services.api import Domain, SearchByDomain, SearchByParentDomain
from asman.domains.services.domain import (
    TableDomain,
    TABLE_DOMAINS_NAME,
)
from asman.domains.services.utils import filter_domains


class DomainRepository(AbstractRepository):
    def __init__(self, database: DatabaseFacade, table_name: str) -> None:
        self.database = database
        self.table_name = table_name

    async def insert(self, entities: Dict[str, List[str]]) -> Sequence[Domain]:
        domains = filter_domains(entities)
        inserted_domains = self.database.upsert(TABLE_DOMAINS_NAME, domains)

        return list(
            map(
                lambda domain: TableDomain.convert(domain),
                inserted_domains,
            )
        )

    async def update(self, entities: Sequence[BaseModel]) -> Sequence[BaseModel]:
        raise NotImplementedException

    async def search(self, filter: Sequence[SearchByDomain] | Sequence[SearchByParentDomain]) -> Sequence[Domain]:
        return list(
            map(
                lambda domain: TableDomain.convert(domain),
                self.database.query(self.table_name, filter)
            )
        )

    async def list(self) -> Sequence[Domain]:
        return list(
            map(
                lambda domain: TableDomain.convert(domain),
                self.database.query(self.table_name)
            )
        )

    async def delete(self, filter: Sequence[SearchByDomain] | Sequence[SearchByParentDomain]) -> Sequence[BaseModel]:
        removed_domains = self.database.delete(self.table_name, filter)

        return list(
            map(
                lambda domain: TableDomain.convert(domain),
                removed_domains,
            )
        )
