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

    def __init__(self, database: Databases):
        if database == Databases.PostgreSQL:
            self._database = Postgres()

        if database == Databases.DynamoDB:
            self._database = DynamoDB()

    def upsert(self, table_name: str, items: List[BaseModel]) -> List:
        # TODO: Возможно, должны быть реализованы обе стратегии — on conflict update и on conflict ignore
        return self._database.upsert(table_name, unique(items))

    def query(self, table_name: str, query: List[BaseModel] = []) -> List[BaseModel]:
        return self._database.items(table_name, query)

    def delete(self, table_name: str, items: List[BaseModel]) -> List:
        return self._database.delete(table_name, items)

    def clear(self, table_name: str) -> List:
        return self._database.delete_all(table_name)
