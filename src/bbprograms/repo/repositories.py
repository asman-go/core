from abc import ABC, abstractmethod
from typing import Optional, Sequence

from src.core.adapters.db import Database
from src.core.exceptions import NotImplementedException
from src.core.arch import AbstractRepository

from ..domain.entities import BugBountyProgramEntity
from ..models import PROGRAMMES_TABLE_NAME



class BugBountyProgramRepository(AbstractRepository):
    def __init__(self, database: Database) -> None:
        self.database = database

    def insert(self, program: BugBountyProgramEntity) -> BugBountyProgramEntity | None:
        raise NotImplementedException

    def update(self, program: BugBountyProgramEntity) -> BugBountyProgramEntity:
        self.database.upsert(PROGRAMMES_TABLE_NAME, program)
        return program

    def get_by_id(self, program_id) -> BugBountyProgramEntity | None:
        raise NotImplementedException

    def delete(self, program_id):
        raise NotImplementedException

    def list(self) -> Sequence[BugBountyProgramEntity] | None:
        raise NotImplementedException
