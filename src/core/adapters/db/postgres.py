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

        if config:
            database_url = ''.join([
                'postgresql+psycopg2://',
                f'{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}',
                '@',
                f'{config.POSTGRES_HOST}:{config.POSTGRES_PORT}',
                '/',
                config.POSTGRES_DB
            ])
            self.logger = logging.getLogger(f'postgres_{config.POSTGRES_DB}')
        else:
            database_url = 'sqlite:///:memory:'
            self.logger = logging.getLogger('sqlite_inmemory')

        # self.database = databases.Database(database_url)
        self.engine = sqlalchemy.create_engine(database_url)
        # Создаем все таблицы
        TableBase.metadata.create_all(self.engine)

    def upsert(self, table_name: str, data: pydantic.BaseModel):
        raise NotImplementedException

    def get_item(self, table_name: str, item_id) -> pydantic.BaseModel:
        raise NotImplementedException
