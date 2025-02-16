from abc import ABC, abstractmethod
from typing import Optional, Sequence

from asman.core.adapters.db import DatabaseFacade
from asman.core.arch import Entity


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, database: DatabaseFacade) -> None:
        ...

    @abstractmethod
    def insert(self, entity: Entity) -> Optional[Entity]:
        ...

    @abstractmethod
    def update(self, entity: Entity) -> Entity:
        ...

    @abstractmethod
    def get_by_id(self, entity_id) -> Optional[Entity]:
        ...

    @abstractmethod
    def delete(self, entity_id):
        ...

    @abstractmethod
    def list(self) -> Optional[Sequence[Entity]]:
        ...
