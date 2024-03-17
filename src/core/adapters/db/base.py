from abc import ABC, abstractmethod
import pydantic
from pydantic_settings import BaseSettings


class Database(ABC):
    @abstractmethod
    def __init__(self, config: BaseSettings, *argv) -> None:
        ...

    @abstractmethod
    def upsert(self, table_name: str, data: pydantic.BaseModel):
        ...

    @abstractmethod
    def get_item(self, table_name: str, item_id) -> pydantic.BaseModel:
        ...
