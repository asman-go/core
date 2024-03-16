import boto3
from moto import mock_dynamodb

from src.core.adapters.db import DynamoDB

REGION_NAME = 'us-east-1'

@mock_dynamodb
def test_dynamodb_instance_create(
        dynamodb_config,
        dynamodb_key_schema,
        dynamodb_attribute_definitions
    ):
    db = DynamoDB(
        dynamodb_config,
        dynamodb_key_schema,
        dynamodb_attribute_definitions,
    )
    
    assert db.key_schema == dynamodb_key_schema
    assert db.attribute_definitions == dynamodb_attribute_definitions
    assert db._client
    assert db._resource
