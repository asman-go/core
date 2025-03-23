from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional, Sequence

from asman.core.adapters.db import DatabaseFacade


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, database: DatabaseFacade, table_name: str) -> None:
        ...

    @abstractmethod
    def insert(self, entities: Sequence[BaseModel]) -> Sequence[BaseModel]:
        ...

    @abstractmethod
    def update(self, entities: Sequence[BaseModel]) -> Sequence[BaseModel]:
        ...

    @abstractmethod
    def search(self, filter: Sequence[BaseModel]) -> Sequence[BaseModel]:
        ...

    @abstractmethod
    def delete(self, filter: Sequence[BaseModel]):
        ...

    @abstractmethod
    def list(self) -> Sequence[BaseModel]:
        ...
