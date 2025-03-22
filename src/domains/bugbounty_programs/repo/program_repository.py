from pydantic import BaseModel
from typing import Sequence

from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import AbstractRepository, Entity
from asman.core.exceptions import NotImplementedException


class ProgramRepository(AbstractRepository):
    def __init__(self, database: DatabaseFacade) -> None:
        self.database = database

    async def insert(self, entities: Sequence[BaseModel]) -> Sequence[BaseModel]:
        raise NotImplementedException

    async def update(self, entities: Sequence[BaseModel]) -> Sequence[BaseModel]:
        raise NotImplementedException

    async def search(self, filter: Sequence[BaseModel]) -> Sequence[BaseModel]:
        raise NotImplementedException

    async def list(self) -> Sequence[BaseModel]:
        raise NotImplementedException

    async def delete(self, filter: Sequence[BaseModel]):
        raise NotImplementedException
