from asman.core.adapters.db.dynamodb import (
    TableBase,

    Key,
    AttributeDefinition,
    ProvisionedThroughput,
)


EXAMPLE_TABLE_NAME = 'example'


class ExampleTable(TableBase):
    table_name = EXAMPLE_TABLE_NAME
    key_schema = [
        Key(
            AttributeName='id',
            KeyType='HASH',
        )
    ]
    attribute_definitions = [
        AttributeDefinition(
            AttributeName='id',
            AttributeType='S',
        ),
        # AttributeDefinition(
        #     AttributeName='address',
        #     AttributeType='S',
        # )
    ]
    provisioned_throughput = ProvisionedThroughput()
