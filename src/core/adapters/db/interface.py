from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Optional


class DatabaseInterface(ABC):
    @abstractmethod
    def __init__(self, *argv) -> None:
        ...

    @abstractmethod
    def upsert(self, table_name: str, data: List[BaseModel]) -> List:
        ...

    @abstractmethod
    def items(self, table_name: str, ids: Optional[List[BaseModel]]) -> List[BaseModel]:
        ...

    @abstractmethod
    def delete(self, table_name: str, data: List[BaseModel]) -> List:
        ...

    @abstractmethod
    def delete_all(self, table_name: str) -> List:
        ...
