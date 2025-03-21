from enum import IntEnum
from pydantic import BaseModel
from typing import List

from .interface import DatabaseInterface
from .postgresql import Postgres
from .dynamodb import DynamoDB
from .utils import unique


class Databases(IntEnum):
    PostgreSQL = 0
    DynamoDB = 1


"""
Какие проблемы тут решим
1. Если я добавляю дубли в рамках одного батча — я получаю ошибку
от базы, так как это моя ответственность принести уникальные объекты
на уровне фасада будет проверять уникальность объектов внутри батча
2. Если upsert на уровне базы невозможен, делаем его на уровне фасада
3. Возможно, должны быть реализованы обе стратегии — on conflict update и on conflict ignore
"""


class DatabaseFacade:
    _database: DatabaseInterface
    _table_name: str | None

    def __init__(self, database: Databases, table_name: str | None = None):
        self._table_name = table_name

        if database == Databases.PostgreSQL:
            self._database = Postgres()

        if database == Databases.DynamoDB:
            self._database = DynamoDB()

    def upsert(self, items: List[BaseModel], table_name: str | None = None) -> List:
        # TODO: Возможно, должны быть реализованы обе стратегии — on conflict update и on conflict ignore

        _table_name = table_name if table_name else self._table_name

        return self._database.upsert(_table_name, unique(items))

    def query(self, query: List[BaseModel] = [], table_name: str | None = None) -> List[BaseModel]:
        _table_name = table_name if table_name else self._table_name
        return self._database.items(_table_name, query)

    def delete(self, items: List[BaseModel], table_name: str | None = None) -> List:
        _table_name = table_name if table_name else self._table_name
        return self._database.delete(_table_name, items)

    def clear(self, table_name: str | None = None) -> List:
        _table_name = table_name if table_name else self._table_name
        return self._database.delete_all(_table_name)
