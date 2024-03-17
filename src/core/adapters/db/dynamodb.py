import boto3
import pydantic
import pydantic_settings

from .base import Database


class DynamoDBConfig(pydantic_settings.BaseSettings):
    DOCUMENT_API_ENDPOINT: str = pydantic.Field(
        default="https://example.com/path/to/your/db"
    )
    REGION_NAME: str = pydantic.Field(default="ru-central1")
    AWS_ACCESS_KEY_ID: str = pydantic.Field(default="<key-id>")
    AWS_SECRET_ACCESS_KEY: str = pydantic.Field(default="<secret-access-key>")


class DynamoDB(Database):

    def __init__(
                self,
                config: DynamoDBConfig,
                key_schema,
                attribute_definitions
            ) -> None:

        self.key_schema = key_schema
        self.attribute_definitions = attribute_definitions

        self._client = boto3.client(
            'dynamodb',
            endpoint_url=config.DOCUMENT_API_ENDPOINT,
            region_name=config.REGION_NAME,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )

        self._resource = boto3.resource(
            'dynamodb',
            endpoint_url=config.DOCUMENT_API_ENDPOINT,
            region_name=config.REGION_NAME,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )

    def _create_table(
                self,
                table_name: str,
                key_schema,
                attribute_definitions
            ):

        table = self._resource.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()

        return table

    def _get_table(
                self,
                table_name: str,
                key_schema,
                attribute_definitions
            ):

        tables = self._client.list_tables()['TableNames']
        if table_name not in tables:
            table = self._create_table(
                table_name,
                key_schema,
                attribute_definitions
            )

            return table
        else:
            return self._resource.Table(table_name)

    def upsert(self, table_name: str, data: pydantic.BaseModel):
        table = self._get_table(
            table_name,
            self.key_schema,
            self.attribute_definitions
        )
        table.put_item(
            Item=data.model_dump()  # data.dict() is deprecated
        )

    def get_item(
                self,
                table_name: str,
                item_id: pydantic.BaseModel
            ) -> pydantic.BaseModel:
        response = self._client.get_item(
            TableName=table_name,
            Key=item_id
        )
        print(response)
        return None
