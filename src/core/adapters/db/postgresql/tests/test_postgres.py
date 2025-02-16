import pytest
import pydantic
import sqlalchemy

from asman.core.adapters.db.postgresql import Postgres, TableBase


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


TABLE_NAME = 'table_debug'


class TableDebug(TableBase):
    __tablename__ = TABLE_NAME

    item = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    debug = sqlalchemy.Column(sqlalchemy.Boolean)

    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('item', 'name'),
    )

    @staticmethod
    def convert(obj: 'TableDebug') -> Item:
        return Item(
            item=obj.item,
            name=obj.name,
            debug=obj.debug,
        )


@pytest.fixture
def init_postgres_envs(monkeypatch):
    monkeypatch.setenv('POSTGRES_DB', 'my_db')
    monkeypatch.setenv('POSTGRES_USER', 'my_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'my_password')
    monkeypatch.setenv('POSTGRES_HOST', 'localhost')
    monkeypatch.setenv('POSTGRES_PORT', '6432')


@pytest.fixture
def postgres_instance(init_postgres_envs) -> Postgres:
    return Postgres()


@pytest.fixture(autouse=True)
def clear_table(postgres_instance):
    # Перед каждым тестом очищаем таблицу
    postgres_instance.delete_all(TABLE_NAME)


def test_postgres_instance_create(init_postgres_envs):
    postgres = Postgres()

    assert postgres


def test_crud(postgres_instance):
    item1 = Item(item='crud-test1', name='name1')
    item2 = Item(item='crud-test2', name='name2', debug=True)

    items = [item1, item2]

    postgres_instance.upsert(TABLE_NAME, items)
    rows = postgres_instance.items(TABLE_NAME)

    assert rows
    assert len(rows) == len(items)
    assert list(map(TableDebug.convert, rows)) == items

    found = postgres_instance.items(TABLE_NAME, [item1, item2])
    assert found
    assert len(found) == 2

    postgres_instance.delete(TABLE_NAME, [item2])
    found = postgres_instance.items(TABLE_NAME, [item2])

    assert not found


# Если я добавляю дубли в рамках разных батчей, то база дубли разрешивает (обновляет поля)
def test_upsert_double_different_batch(postgres_instance):
    item1 = Item(item='upsert-test1', name='name1')
    item2 = Item(item='upsert-test2', name='name2', debug=True)
    item3 = Item(item='upsert-test1', name='name3')
    item4 = Item(item='upsert-test1', name='name1', debug=True)

    items1 = [item1, item2]
    items2 = [item3, item4]

    postgres_instance.upsert(TABLE_NAME, items1)
    rows = postgres_instance.items(TABLE_NAME)

    assert len(rows) == len(items1)

    postgres_instance.upsert(TABLE_NAME, items2)
    rows = postgres_instance.items(TABLE_NAME)

    assert len(rows) == len(items1) + len(items2) - 1

    found = postgres_instance.items(TABLE_NAME, [item1])
    assert not found, "Старая запись осталась, хотя должна была обновиться"

    found = postgres_instance.items(TABLE_NAME, [item4])
    assert found, "Запись не обновилась, а почему-то осталась старая запись"


# Если я добавляю дубли в рамках одного батча — я получаю ошибку от базы, так как это моя ответственность принести уникальные объекты
def test_upsert_double_same_batch_raise_exception(postgres_instance):
    item1 = Item(item='exc-test1', name='name1')
    item2 = Item(item='exc-test2', name='name2', debug=True)
    item3 = Item(item='exc-test1', name='name3')
    item4 = Item(item='exc-test1', name='name1', debug=True)

    items = [item1, item2, item3, item4]

    with pytest.raises(sqlalchemy.exc.ProgrammingError):
        postgres_instance.upsert(TABLE_NAME, items)


def test_delete_not_existed(postgres_instance):
    item1 = Item(item='delete-test1', name='name1')
    item2 = Item(item='delete-test2', name='name2', debug=True)
    postgres_instance.upsert(TABLE_NAME, [item1, item2])

    rows = postgres_instance.items(TABLE_NAME)
    assert len(rows) == 2

    postgres_instance.delete(TABLE_NAME, [item1])
    rows = postgres_instance.items(TABLE_NAME)
    assert len(rows) == 1

    postgres_instance.delete(TABLE_NAME, [item1])
    rows = postgres_instance.items(TABLE_NAME)
    assert len(rows) == 1


def test_table_name_is_none_raise_exception(postgres_instance):
    item1 = Item(item='delete-test1', name='name1')

    with pytest.raises(AssertionError):
        postgres_instance.upsert(None, [item1])

    with pytest.raises(AssertionError):
        _ = postgres_instance.items(None)

    with pytest.raises(AssertionError):
        postgres_instance.delete(None, [item1])
