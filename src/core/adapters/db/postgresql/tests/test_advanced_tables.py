import pytest
from pydantic import create_model
from sqlalchemy.dialects.postgresql import insert

from asman.core.adapters.db.postgresql.tests import (
    Child, Parent,
    # TableChild, TableParent,
    TABLE_CHILDREN_NAME,
    TABLE_PARENTS_NAME,
    TABLE_PARENT_CHILD_ASSOCIATION_NAME,
)
from asman.core.adapters.db.postgresql.utils import (
    get_autoincrement,
    get_unique_constraints,
)


def test_crud(postgres_instance):
    child1 = Child(
        name='Child'
    )
    parent1 = Parent(
        name='Father',
        address='City, Address, 1',
    )
    parent2 = Parent(
        name='Mother',
        address='City, Address, 1',
    )

    _Association = create_model('Association', parent_id=(int, ...), child_id=(int, ...))

    parents_primary_keys = postgres_instance.upsert(TABLE_PARENTS_NAME, [parent1, parent2])
    assert len(parents_primary_keys) == 2

    children_primary_keys = postgres_instance.upsert(TABLE_CHILDREN_NAME, [child1])
    assert len(children_primary_keys) == 1

    _ = postgres_instance.upsert(TABLE_PARENT_CHILD_ASSOCIATION_NAME, [
        _Association(**{
            'child_id': children_primary_keys[0][0],
            'parent_id': parents_primary_keys[0][0],
        }),
        _Association(**{
            'child_id': children_primary_keys[0][0],
            'parent_id': parents_primary_keys[1][0],
        }),
    ])

    rows = postgres_instance.items(TABLE_CHILDREN_NAME)

    assert len(rows) == 1


def _test_get_upsert_stmt(postgres_instance):
    # Для дебага
    parent1 = Parent(
        name='Father',
        address='City, Address, 1',
    )
    data = [parent1]
    table = postgres_instance._get_table(TABLE_PARENTS_NAME)
    stmt = (
        insert(table)
        .values(
            list(
                map(
                    lambda item: item.model_dump(
                        include=item.model_fields.keys() & table.columns.keys(),
                    ),
                    data
                )
            )
        )
    )
    print('WTF', get_unique_constraints(table))
    set_ = dict()

    for column in table.columns:
        print('Colume', column, column.autoincrement)
        if column.autoincrement != True:
            set_[column.name] = stmt.excluded[column.name]
    
    print('WTF2', set_)

    stmt = stmt.on_conflict_do_update(
        index_elements=get_unique_constraints(table),
        set_=set_,
    )
    stmt = stmt.compile(compile_kwargs={'literal_binds': True})
    assert str(stmt) == 1
