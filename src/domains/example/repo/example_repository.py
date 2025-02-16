import pydantic
from typing import Sequence
from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import AbstractRepository
from asman.core.exceptions import NotImplementedException

from ..domain.example_entity import ExampleEntity


class _Search(pydantic.BaseModel):
    id: str = pydantic.Field()


class ExampleRepository(AbstractRepository):
    def __init__(self, database: DatabaseFacade, table_name: str) -> None:
        self.database = database
        self.table_name = table_name

    def insert(self, entity: ExampleEntity) -> ExampleEntity | None:
        raise NotImplementedException

    def update(self, entity: ExampleEntity) -> ExampleEntity:
        self.database.upsert([entity], self.table_name)
        found = self.database.query([entity], self.table_name)[0]

        return pydantic.TypeAdapter(ExampleEntity).validate_python(found)

    def get_by_id(self, entity_id) -> ExampleEntity | None:
        search = _Search(id=entity_id)
        found = self.database.query([search], self.table_name)

        if found and len(found) == 1:
            return pydantic.TypeAdapter(ExampleEntity).validate_python(found[0])

        return None

    def delete(self, entity_id):
        raise NotImplementedException

    def list(self) -> Sequence[ExampleEntity] | None:
        raise NotImplementedException
