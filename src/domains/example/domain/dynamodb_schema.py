DYNAMODB_TABLE_NAME = 'example'

DYNAMODB_KEY_SCHEMA = [
    {
        'AttributeName': 'id',
        'KeyType': 'HASH'
    }
]

DYNAMODB_ATTRIBUTE_DEFINITIONS = [
    {
        'AttributeName': 'id',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'address',
        'AttributeType': 'S'
    }
]
