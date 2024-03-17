from typing import Sequence
from asman.core.adapters.db.base import Database
from asman.core.arch import AbstractRepository
from asman.core.exceptions import NotImplementedException

from ..domain.example_entity import ExampleEntity


class ExampleRepository(AbstractRepository):
    def __init__(self, database: Database, table_name: str) -> None:
        self.database = database
        self.table_name = table_name

    def insert(self, entity: ExampleEntity) -> ExampleEntity | None:
        raise NotImplementedException

    def update(self, entity: ExampleEntity) -> ExampleEntity:
        self.database.upsert(self.table_name, entity)
        return entity

    def get_by_id(self, entity_id) -> ExampleEntity | None:
        return self.database.get_item(self.table_name, entity_id)

    def delete(self, entity_id):
        raise NotImplementedException

    def list(self) -> Sequence[ExampleEntity] | None:
        raise NotImplementedException
