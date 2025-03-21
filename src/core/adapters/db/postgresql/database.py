import logging
import sqlalchemy
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, declarative_base
from typing import List

from .config import PostgresConfig
from .utils import (
    make_stmt,
    get_unique_constraints,
    get_autoincrement,
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

    def upsert(self, table_name, data) -> List:
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
                            lambda item: item.model_dump(
                                # В модели могут быть другие поля, добавляем только табличные (при этом сгенерированные табличные не пишем)
                                include=item.model_fields.keys() & table.columns.keys(),
                            ),
                            data
                        )
                    )
                )
            )

            constraints = get_unique_constraints(table)
            set_ = dict()
            for column in table.columns:
                if column.autoincrement != True and column.name not in constraints:
                    set_[column.name] = stmt.excluded[column.name]

            if constraints:
                if set_:
                    # Чтобы использовать эту функцию, надо использовать insert из диалекта postgres, а не общую
                    stmt = stmt.on_conflict_do_update(
                        index_elements=constraints,
                        # set_=table.columns,  # Оставить старые поля == on_conflict_do_nothing
                        # set_=stmt.excluded,  # Оставить новые поля == upsert
                        set_=set_,  # Оставить новые поля == upsert, автоикременты не обновляем (в модели null будет — ошибка) и вообще все unique и PK?
                    )
                else:
                    stmt = stmt.on_conflict_do_nothing(
                        index_elements=constraints,
                    )

            stmt = stmt.returning(
                *table.primary_key.columns.values(),
            )

            result = session.execute(stmt)
            session.commit()

            return result.fetchall()

    def delete(self, table_name, data) -> List:
        # Получаем класс ORM модели по имени таблицы
        table = self._get_table(table_name)

        with Session(self.engine) as session:
            stmt = (
                sqlalchemy.delete(table)
                .where(
                    make_stmt(
                        table,
                        *data
                    ) if data else False
                )
                .returning(
                    *table.primary_key.columns.values(),
                )
            )

            result = session.execute(stmt)
            session.commit()

            return result.fetchall()

    def delete_all(self, table_name) -> List:
        table = self._get_table(table_name)

        with Session(self.engine) as session:
            stmt = (
                sqlalchemy.delete(
                    table
                ).returning(
                    *table.primary_key.columns.values(),
                )
            )
            result = session.execute(stmt)
            session.commit()

            return result.fetchall()

    def items(self, table_name, ids=None) -> List:
        table = self._get_table(table_name)

        with Session(self.engine) as session:
            return (
                session
                .query(table)
                .where(
                    make_stmt(table, *ids) if ids else True
                )
                .all()
            )
