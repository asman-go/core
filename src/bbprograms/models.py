# DynamoDB Schema

# Таблица, в которой храним BB программы
PROGRAMMES_TABLE_NAME = 'bbprogrammes'

# Схема ключей таблицы PROGRAMMES_TABLE_NAME
PROGRAMMES_TABLE_KEY_SCHEMA = [
    {
        'AttributeName': 'program_site',
        'KeyType': 'HASH'
    }
]

# Схема столбцов таблицы PROGRAMMES_TABLE_NAME
PROGRAMMES_TABLE_ATTRIBUTE_DEFINITIONS = [
    {
        'AttributeName': 'program_name',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'program_site',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'platform',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'in_scope',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'mobile_scope',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'not_paid_scope',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'out_of_scope',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'notes',
        'AttributeType': 'S'
    },
]
