from botocore.exceptions import ClientError
import pytest
import pydantic

from asman.core.adapters.db.dynamodb import (
    DynamoDB,
    TableBase,

    Key,
    AttributeDefinition,
    ProvisionedThroughput,
)


TABLE_NAME = 'table_debug'


class Item(pydantic.BaseModel):
    model_config = {"frozen": True}
    item: str = pydantic.Field()
    name: str = pydantic.Field()
    debug: bool = pydantic.Field(default=False)

    def __eq__(self, value):
        return isinstance(value, Item) and self.item == value.item and self.name == value.name

    def __hash__(self):
        return hash(str(
            {
                "item": self.item,
                "name": self.name,
            }
        ))


class TableDebug(TableBase):
    table_name = TABLE_NAME
    key_schema = [
        Key(
            AttributeName='item',
            KeyType='HASH'
        ),
        Key(
            AttributeName='name',
            KeyType='RANGE'
        ),
    ]
    attribute_definitions = [
        AttributeDefinition(
            AttributeName='item',
            AttributeType='S',
        ),
        AttributeDefinition(
            AttributeName='name',
            AttributeType='S',
        ),
        # AttributeDefinition(
        #     AttributeName='debug',
        #     AttributeType='N',
        # ),
    ]
    provisioned_throughput = ProvisionedThroughput()


@pytest.fixture
def init_dynamodb_envs(monkeypatch):
    monkeypatch.setenv('DOCUMENT_API_ENDPOINT', 'http://localhost:8000')
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', '12345')


@pytest.fixture
def dynamodb_instance(init_dynamodb_envs) -> DynamoDB:
    return DynamoDB()


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

    _items = pydantic.TypeAdapter(list[Item]).validate_python(found)
    
    assert _items, 'Данные из таблицы не десериализовались в Item объект'
    assert len(_items) == len(items), 'Количество элементов не совпало'

    for _item in _items:
        assert _item in items, f'Объект {_item} не обнаружен в начальном списке'

    # Поиск элементов

    found = dynamodb_instance.items(TABLE_NAME, [item1])

    assert found, f'Не нашли элемент {item1}'
    assert len(found) == 1, 'Ищем по ключу, должен быть один элемент'

    _item = pydantic.TypeAdapter(Item).validate_python(found[0])

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
