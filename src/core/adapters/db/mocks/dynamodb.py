import mock
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from src.core.adapters.db import DynamoDB


class MockDynamoDB(DynamoDB):
    localDB: dict

    def __init__(
            self,
            config: BaseModel, 
            key_schema, 
            attribute_definitions
        ) -> None:
        self.key_schema = key_schema
        self.attribute_definitions = attribute_definitions

        self.localDB = dict()

        self._client = mock.Mock()
        self._resource = mock.Mock()

    def upsert(self, table_name: str, data: BaseModel):
        self.localDB[data.id] = data
        return data
    
    def get_item(self, table_name: str, item_id: BaseModel) -> BaseModel:
        return self.localDB[item_id['id']['S']]
