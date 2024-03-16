from src.core.adapters.db import DynamoDBConfig


def test_dynamodb_config_create(monkeypatch):
    DOCUMENT_API_ENDPOINT = '1'
    REGION_NAME = '2'
    AWS_ACCESS_KEY_ID = '3'
    AWS_SECRET_ACCESS_KEY = '4'

    monkeypatch.setenv('DOCUMENT_API_ENDPOINT', DOCUMENT_API_ENDPOINT)
    monkeypatch.setenv('REGION_NAME', REGION_NAME)
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', AWS_ACCESS_KEY_ID)
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', AWS_SECRET_ACCESS_KEY)

    config = DynamoDBConfig()

    assert config
    assert config.DOCUMENT_API_ENDPOINT == DOCUMENT_API_ENDPOINT
    assert config.REGION_NAME == REGION_NAME
    assert config.AWS_ACCESS_KEY_ID == AWS_ACCESS_KEY_ID
    assert config.AWS_SECRET_ACCESS_KEY == AWS_SECRET_ACCESS_KEY
