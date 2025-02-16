import pydantic
from typing import Dict, List, Optional, Iterable


class ProvisionedThroughput(pydantic.BaseModel):
    ReadCapacityUnits: int = pydantic.Field(default=25)
    WriteCapacityUnits: int = pydantic.Field(default=25)


class Key(pydantic.BaseModel):
    AttributeName: str = pydantic.Field()
    KeyType: str = pydantic.Field()


class AttributeDefinition(pydantic.BaseModel):
    AttributeName: str = pydantic.Field()
    AttributeType: str = pydantic.Field()


class _Table(pydantic.BaseModel):
    table_name: str = pydantic.Field()
    key_schema: List[Key] = pydantic.Field(default_factory=lambda: list())
    attribute_definitions: List[AttributeDefinition] = pydantic.Field(default_factory=lambda: list())
    provisioned_throughput: ProvisionedThroughput = pydantic.Field(
        default=ProvisionedThroughput(
            ReadCapacityUnits=5,
            WriteCapacityUnits=5,
        )
    )


class _MetaData:
    _instance = None
    _tables: Dict[str, _Table]

    def __new__(cls):
        # Singletone
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_tables'):
            self._tables = dict()

    def add(self, table_name: str, table: _Table):
        self._tables[table_name] = table.model_copy()

    def get(self, table_name: str) -> _Table | None:
        if table_name in self._tables:
            return self._tables[table_name]

        return None

    @property
    def tables(self) -> Iterable[tuple[str, _Table]]:
        return self._tables.items()


class _DeclarativeBase(type):
    def __new__(cls, *args, **kwargs):

        TABLE_NAME = 'table_name'
        KEY_SCHEMA = 'key_schema'
        ATTRIBUTE_DEFINITIONS = 'attribute_definitions'
        PROVISIONED_THROUGHPUT = 'provisioned_throughput'

        # Создаем класс
        self = super().__new__(cls, *args, **kwargs)

        if (hasattr(self, TABLE_NAME)
            and hasattr(self, KEY_SCHEMA)
            and hasattr(self, ATTRIBUTE_DEFINITIONS)
            and hasattr(self, PROVISIONED_THROUGHPUT)
        ):
            _MetaData().add(
                getattr(self, TABLE_NAME),
                _Table(
                    table_name=getattr(self, TABLE_NAME),
                    key_schema=pydantic.TypeAdapter(List[Key]).validate_python(getattr(self, KEY_SCHEMA)),
                    attribute_definitions=pydantic.TypeAdapter(List[AttributeDefinition]).validate_python(getattr(self, ATTRIBUTE_DEFINITIONS)),
                    provisioned_throughput=pydantic.TypeAdapter(ProvisionedThroughput).validate_python(getattr(self, PROVISIONED_THROUGHPUT)),
                ),
            )

        return self


class Base(metaclass=_DeclarativeBase):
    metadata: _MetaData = _MetaData()


# class TableDebug(Base):
#     table_name = 'bla'
#     key_schema = [
#         Key(
#             AttributeName='item',
#             KeyType='HASH'
#         ),
#         Key(
#             AttributeName='name',
#             KeyType='RANGE'
#         ),
#         Key(
#             AttributeName='debug',
#             KeyType='RANGE'
#         ),
#     ]
#     attribute_definitions = [
#         AttributeDefinition(
#             AttributeName='item',
#             AttributeType='S',
#         ),
#         AttributeDefinition(
#             AttributeName='name',
#             AttributeType='S',
#         ),
#         AttributeDefinition(
#             AttributeName='debug',
#             AttributeType='N',
#         ),
#     ]
#     provisioned_throughput = ProvisionedThroughput()


# if __name__ == '__main__':
#     print('Hello', TableDebug.metadata.tables, _MetaData().tables)
