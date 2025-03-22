import pytest
from pydantic import BaseModel, Field

from asman.core.adapters.db.dynamodb import (
    DynamoDB,
    TableBase,

    Key,
    AttributeDefinition,
    ProvisionedThroughput,
)


TABLE_NAME = 'table_debug'


class Item(BaseModel):
    model_config = {"frozen": True}
    item: str = Field()
    name: str = Field()
    debug: bool = Field(default=False)

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
