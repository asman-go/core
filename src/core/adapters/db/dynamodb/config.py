import pydantic
from pydantic_settings import BaseSettings


class DynamoDBConfig(BaseSettings):
    DOCUMENT_API_ENDPOINT: str = pydantic.Field(
        default="https://example.com/path/to/your/db"
    )
    REGION_NAME: str = pydantic.Field(default="ru-central1")
    AWS_ACCESS_KEY_ID: str = pydantic.Field(default="<key-id>")
    AWS_SECRET_ACCESS_KEY: str = pydantic.Field(default="<secret-access-key>")
