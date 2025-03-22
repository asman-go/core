from pydantic import BaseModel, Field, TypeAdapter
from typing import Sequence
from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import AbstractRepository
from asman.core.exceptions import NotImplementedException

from ..domain.example_entity import ExampleEntity, ExampleData
from asman.domains.example.api import SearchFilter


class ExampleRepository(AbstractRepository):
    def __init__(self, database: DatabaseFacade) -> None:
        self.database = database

    def insert(self, entities: Sequence[ExampleData]) -> Sequence[ExampleEntity]:
        raise NotImplementedException

    def update(self, entities: Sequence[ExampleData]) -> Sequence[ExampleEntity]:
        self.database.upsert(entities)
        found = self.database.query(entities)

        return TypeAdapter(Sequence[ExampleEntity]).validate_python(found)

    def search(self, filter: Sequence[SearchFilter]) -> Sequence[ExampleEntity]:
        print('Example Repo Search Filter', filter, filter[0])
        found = self.database.query(filter)

        return TypeAdapter(Sequence[ExampleEntity]).validate_python(found)

    def delete(self, filter: Sequence[SearchFilter]):
        raise NotImplementedException

    def list(self) -> Sequence[ExampleEntity]:
        raise NotImplementedException
