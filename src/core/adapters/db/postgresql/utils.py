import functools
import pydantic
import sqlalchemy
import typing


def _unit_column_elements_or(*elements: sqlalchemy.ColumnElement) -> sqlalchemy.ColumnElement:
    return functools.reduce(
        lambda a, b: sqlalchemy.or_(a, b),
        elements
    )


def _unit_column_elements_and(*elements: sqlalchemy.ColumnElement) -> sqlalchemy.ColumnElement:
    return functools.reduce(
        lambda a, b: sqlalchemy.and_(a, b),
        elements
    )


def get_unique_constraints(table: sqlalchemy.Table) -> typing.List[str]:
    """
        Возвращает имена столбцов, которые уникальные или primary key, но не автоинкрементальные
    """

    unique_columns = set()

    # Добавляем PRIMARY KEY
    primary_keys = [column.name for column in table.primary_key.columns if column.autoincrement != True]  # autoincrement может быть True, False, auto
    unique_columns.update(primary_keys)

    # Добавляем UNIQUE ограничения
    for constraint in table.constraints:
        if constraint.__class__.__name__ == "UniqueConstraint":
            unique_columns.update([col.name for col in constraint.columns])

    return list(unique_columns)


def get_autoincrement(table: sqlalchemy.Table) -> typing.List[str]:
    """
        Возвращаем имена автоинкрементных столцов (primary key)
    """
    return [column.name for column in table.primary_key.columns if column.autoincrement]


# items -> (a and b and c) or (d and e) or ...
# item — пары столбец-значение, они объединяются через AND
def make_stmt(table: sqlalchemy.Table, *items: pydantic.BaseModel) -> sqlalchemy.ColumnElement:

    def _make_part_of_stmt(item: pydantic.BaseModel) -> sqlalchemy.ColumnElement:
        data = item.model_dump()

        return _unit_column_elements_and(
            *list(
                map(
                    lambda column_name: table.columns[column_name] == data[column_name],
                    data.keys()
                )
            )
        )

    return _unit_column_elements_or(
        *list(
            map(
                lambda item: _make_part_of_stmt(item),
                items
            )
        )
    )
