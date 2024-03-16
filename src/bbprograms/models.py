# DynamoDB Schema

PROGRAMMES_TABLE_NAME = 'bbprogrammes'      # Таблица, в которой храним BB программы
PROGRAMMES_TABLE_KEY_SCHEMA = [             # Схема ключей таблицы PROGRAMMES_TABLE_NAME
    {
        'AttributeName': 'program_site',
        'KeyType': 'HASH'
    }
]
PROGRAMMES_TABLE_ATTRIBUTE_DEFINITIONS = [  # Схема столбцов таблицы PROGRAMMES_TABLE_NAME
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