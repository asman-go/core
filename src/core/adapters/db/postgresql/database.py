import logging
import sqlalchemy
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, declarative_base

from .config import PostgresConfig
from .utils import (
    _make_stmt,
    _get_unique_constraints,
)
from ..interface import DatabaseInterface


# Объект, который собирает в себя все метаданные о других таблицах
TableBase = declarative_base()


class Postgres(DatabaseInterface):
    logger: logging.Logger

    def __init__(self):
        config = PostgresConfig()

        database_url = ''.join([
            'postgresql+psycopg2://',
            f'{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}',
            '@',
            f'{config.POSTGRES_HOST}:{config.POSTGRES_PORT}',
            '/',
            config.POSTGRES_DB
        ])
        self.logger = logging.getLogger(f'postgres_{config.POSTGRES_DB}')

        self.engine = sqlalchemy.create_engine(database_url)
        # Создаем все таблицы
        TableBase.metadata.create_all(self.engine)

    def _get_table(self, name: str) -> sqlalchemy.Table:
        return sqlalchemy.Table(name, TableBase.metadata, autoload_with=self.engine)

    def upsert(self, table_name, data):
        # Получаем класс таблицы по имени таблицы
        table = self._get_table(table_name)

        with Session(self.engine) as session:
            stmt = (
                insert(
                    table
                )
                .values(
                    list(
                        map(
                            lambda item: item.model_dump(),
                            data
                        )
                    )
                )
            )
            # Чтобы использовать эту функцию, надо использовать insert из диалекта postgres, а не общую
            stmt = stmt.on_conflict_do_update(
                index_elements=_get_unique_constraints(table),
                # set_=table.columns,  # Оставить старые поля == on_conflict_do_nothing
                set_=stmt.excluded,  # Оставить новые поля == upsert
            )

            session.execute(stmt)
            session.commit()

    def delete(self, table_name, data):
        # Получаем класс ORM модели по имени таблицы
        table = self._get_table(table_name)

        with Session(self.engine) as session:
            stmt = (
                sqlalchemy.delete(table)
                .where(
                    _make_stmt(
                        table,
                        *data
                    ) if data else False
                )
            )

            session.execute(stmt)
            session.commit()

    def delete_all(self, table_name):

        with Session(self.engine) as session:
            stmt = sqlalchemy.delete(
                self._get_table(table_name)
            )
            session.execute(stmt)
            session.commit()

    def items(self, table_name, ids=None):
        table = self._get_table(table_name)

        with Session(self.engine) as session:
            return (
                session
                .query(table)
                .where(
                    _make_stmt(table, *ids) if ids else True
                )
                .all()
            )

        return super().items(table_name, ids)
