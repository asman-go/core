import pytest
import sqlalchemy

from asman.core.adapters.db.postgresql.tests import (
    Child, Parent,
    TableChild, TableParent,
    TABLE_CHILDREN_NAME,
    TABLE_PARENTS_NAME,
    TABLE_PARENT_CHILD_ASSOCIATION_NAME,
)
from asman.core.adapters.db.postgresql import TableBase
from asman.core.adapters.db.postgresql.utils import (
    get_autoincrement,
    get_unique_constraints,
)


def _get_table(table_name: str, postgres_instance) -> sqlalchemy.Table:
    return sqlalchemy.Table(
        table_name,
        TableBase.metadata,
        autoload_with=postgres_instance.engine,
    )


def test_get_unique_constraints(postgres_instance):
    table = _get_table(TABLE_PARENTS_NAME, postgres_instance)
    constraints = get_unique_constraints(table)

    assert 'name' in constraints
    assert 'id' not in constraints


def test_get_autoincrement(postgres_instance):
    table = _get_table(TABLE_PARENTS_NAME, postgres_instance)
    columns = get_autoincrement(table)

    assert len(columns) == 1
    assert 'id' in columns
