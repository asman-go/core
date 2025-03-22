import pytest
import sqlalchemy

from asman.core.adapters.db.postgresql import Postgres
from asman.core.adapters.db.postgresql.tests import Item, TableDebug, TABLE_DEBUG_NAME


def test_postgres_instance_create(init_postgres_envs):
    postgres = Postgres()

    assert postgres


def test_crud(postgres_instance):
    item1 = Item(item='crud-test1', name='name1')
    item2 = Item(item='crud-test2', name='name2', debug=True)

    items = [item1, item2]

    res = postgres_instance.upsert(TABLE_DEBUG_NAME, items)
    assert (item1.item, item1.name) in res
    assert (item2.item, item2.name) in res

    rows = postgres_instance.items(TABLE_DEBUG_NAME)

    assert rows
    assert len(rows) == len(items)
    assert list(map(TableDebug.convert, rows)) == items

    found = postgres_instance.items(TABLE_DEBUG_NAME, [item1, item2])
    assert found
    assert len(found) == 2

    res = postgres_instance.delete(TABLE_DEBUG_NAME, [item2])
    assert (item2.item, item2.name) in res
    found = postgres_instance.items(TABLE_DEBUG_NAME, [item2])

    assert not found


# Если я добавляю дубли в рамках разных батчей, то база дубли разрешивает (обновляет поля)
def test_upsert_double_different_batch(postgres_instance):
    item1 = Item(item='upsert-test1', name='name1')
    item2 = Item(item='upsert-test2', name='name2', debug=True)
    item3 = Item(item='upsert-test1', name='name3')
    item4 = Item(item='upsert-test1', name='name1', debug=True)

    items1 = [item1, item2]
    items2 = [item3, item4]

    primary_keys_1 = postgres_instance.upsert(TABLE_DEBUG_NAME, items1)
    assert len(primary_keys_1) == len(items1)

    primary_keys_2 = postgres_instance.upsert(TABLE_DEBUG_NAME, items2)
    assert len(primary_keys_2) == len(items2)
    rows = postgres_instance.items(TABLE_DEBUG_NAME)

    assert len(rows) == len(items1) + len(items2) - 1

    found = postgres_instance.items(TABLE_DEBUG_NAME, [item1])
    assert not found, "Старая запись осталась, хотя должна была обновиться"

    found = postgres_instance.items(TABLE_DEBUG_NAME, [item4])
    assert found, "Запись не обновилась, а почему-то осталась старая запись"


# Если я добавляю дубли в рамках одного батча — я получаю ошибку от базы, так как это моя ответственность принести уникальные объекты
def test_upsert_double_same_batch_raise_exception(postgres_instance):
    item1 = Item(item='exc-test1', name='name1')
    item2 = Item(item='exc-test2', name='name2', debug=True)
    item3 = Item(item='exc-test1', name='name3')
    item4 = Item(item='exc-test1', name='name1', debug=True)

    items = [item1, item2, item3, item4]

    with pytest.raises(sqlalchemy.exc.ProgrammingError):
        postgres_instance.upsert(TABLE_DEBUG_NAME, items)


def test_delete_not_existed(postgres_instance):
    item1 = Item(item='delete-test1', name='name1')
    item2 = Item(item='delete-test2', name='name2', debug=True)
    primary_keys = postgres_instance.upsert(TABLE_DEBUG_NAME, [item1, item2])

    assert len(primary_keys) == 2

    primary_keys = postgres_instance.delete(TABLE_DEBUG_NAME, [item1])
    assert len(primary_keys) == 1

    rows = postgres_instance.items(TABLE_DEBUG_NAME)
    assert len(rows) == 1

    primary_keys = postgres_instance.delete(TABLE_DEBUG_NAME, [item1])
    assert len(primary_keys) == 0

    rows = postgres_instance.items(TABLE_DEBUG_NAME)
    assert len(rows) == 1


def test_table_name_is_none_raise_exception(postgres_instance):
    item1 = Item(item='delete-test1', name='name1')

    with pytest.raises(AssertionError):
        postgres_instance.upsert(None, [item1])

    with pytest.raises(AssertionError):
        _ = postgres_instance.items(None)

    with pytest.raises(AssertionError):
        postgres_instance.delete(None, [item1])
