import databases
import logging
import pydantic
from pydantic_settings import BaseSettings
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import ClauseElement

from .base import Database

from asman.core.exceptions import NotImplementedException


# Объект, который собирает в себя все метаданные о других таблицах
TableBase = declarative_base()


class PostgresConfig(BaseSettings):
    POSTGRES_DB: str = pydantic.Field()
    POSTGRES_USER: str = pydantic.Field()
    POSTGRES_PASSWORD: str = pydantic.Field()
    POSTGRES_HOST: str = pydantic.Field(
        default='localhost'
    )
    POSTGRES_PORT: int = pydantic.Field(
        default=5432
    )


class Postgres(Database):
    database: databases.Database
    logger: logging.Logger

    def __init__(self, config: PostgresConfig) -> None:
        self.logger = logging.getLogger(f'postgres_{config.POSTGRES_DB}')
        database_url = f'postgresql+psycopg2://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}'
        self.database = databases.Database(database_url)
        self._engine = sqlalchemy.create_engine(database_url)

    async def connect(self):
        await self.database.connect()
        self.logger.debug(f'Connect to database')

    async def disconnect(self):
        await self.database.disconnect()
        self.logger.debug(f'Disconnect from database')

    async def execute(self, query: ClauseElement):
        return await self.database.execute(query)

    async def fetch_one(self, query: ClauseElement):
        return await self.database.fetch_one(query)

    def upsert(self, table_name: str, data: pydantic.BaseModel):
        raise NotImplementedException

    def get_item(self, table_name: str, item_id) -> pydantic.BaseModel:
        raise NotImplementedException
