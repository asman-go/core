from botocore.exceptions import ClientError
import pytest
from pydantic import TypeAdapter

from asman.core.adapters.db.dynamodb import (
    DynamoDB,
)
from asman.core.adapters.db.dynamodb.tests import (
    TABLE_NAME,
    Item,
    TableDebug,
)


@pytest.fixture(autouse=True)
def clear_table(dynamodb_instance):
    # Перед каждым тестом очищаем таблицу
    dynamodb_instance.delete_all(TABLE_NAME)


def test_dynamodb_instance_create(init_dynamodb_envs):
    db = DynamoDB()

    assert db


def test_crud(dynamodb_instance):
    item1 = Item(item='crud-test1', name='name1')
    item2 = Item(item='crud-test2', name='name2', debug=True)

    items = [item1, item2,]

    # Добавление елементов и получение всех элементов

    dynamodb_instance.upsert(TABLE_NAME, items)
    found = dynamodb_instance.items(TABLE_NAME)

    assert found, 'Не получили данные из таблицы ' + TABLE_NAME

    _items = TypeAdapter(list[Item]).validate_python(found)
    
    assert _items, 'Данные из таблицы не десериализовались в Item объект'
    assert len(_items) == len(items), 'Количество элементов не совпало'

    for _item in _items:
        assert _item in items, f'Объект {_item} не обнаружен в начальном списке'

    # Поиск элементов

    found = dynamodb_instance.items(TABLE_NAME, [item1])

    assert found, f'Не нашли элемент {item1}'
    assert len(found) == 1, 'Ищем по ключу, должен быть один элемент'

    _item = TypeAdapter(Item).validate_python(found[0])

    assert _item, 'Данные из таблицы не десериализовались в Item объект'
    assert _item == item1

    # Удаление элементов

    dynamodb_instance.delete(TABLE_NAME, [item1])
    found = dynamodb_instance.items(TABLE_NAME, [item1])

    assert not found, f'Элемент {item1} остался в таблице ({found})'

    # Удаление не существующего элемента
    dynamodb_instance.delete(TABLE_NAME, [item1])

    # Удаление всех элементов

    found = dynamodb_instance.items(TABLE_NAME)
    assert found

    dynamodb_instance.delete_all(TABLE_NAME)
    found = dynamodb_instance.items(TABLE_NAME)
    assert not found


def test_upsert_doubles_same_batch_raise_exception(dynamodb_instance):
    item1 = Item(item='crud-test1', name='name1')
    item2 = Item(item='crud-test1', name='name1', debug=True)

    items = [item1, item2,]

    with pytest.raises(ClientError):
        # Дубли в одном батче вызывают исключение
        dynamodb_instance.upsert(TABLE_NAME, items)


def test_upsert_doubles_different_batch(dynamodb_instance):
    item1 = Item(item='crud-test1', name='name1')
    item2 = Item(item='crud-test1', name='name1', debug=True)

    dynamodb_instance.upsert(TABLE_NAME, [item1])
    dynamodb_instance.upsert(TABLE_NAME, [item2])
    found = dynamodb_instance.items(TABLE_NAME)

    assert found
    assert len(found) == 1, 'Второй элемент должен переписать'
