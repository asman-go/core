import boto3
import logging
import typing

from .config import DynamoDBConfig
from .table import _MetaData, _Table
from ..interface import DatabaseInterface


class DynamoDB(DatabaseInterface):
    logger: logging.Logger

    def __init__(self):
        config = DynamoDBConfig()
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

        for name, table in _MetaData().tables:
            if name not in self._client.list_tables()['TableNames']:
                self._create_table(name, table)

    def _create_table(
                self,
                table_name: str,
                table: _Table,
            ):

        _table = self._resource.create_table(
            TableName=table_name,
            KeySchema=[key.model_dump() for key in table.key_schema],
            AttributeDefinitions=[attr.model_dump() for attr in table.attribute_definitions],
            ProvisionedThroughput=table.provisioned_throughput.model_dump()
        )
        _table.wait_until_exists()

        return _table

    def _get_table(
                self,
                table_name: str,
            ):

        tables = self._client.list_tables()['TableNames']
        if table_name not in tables:
            table = self._create_table(
                table_name,
                _MetaData().get(table_name),
            )

            return table
        else:
            return self._resource.Table(table_name)

    def _get_filter(self, table_name: str, id: dict) -> dict[str, typing.Any]:
        table = _MetaData().get(table_name)
        search = dict()

        for key in table.key_schema:
            if key.AttributeName in id:
                search[key.AttributeName] = id[key.AttributeName]

        return search

    def upsert(self, table_name, data) -> typing.List:
        table = self._get_table(table_name)
        # table.put_item(Item=data.model_dump())  # put 1 item

        with table.batch_writer() as batch:
            return [
                batch.put_item(
                    Item=item.model_dump()
                )
                for item in data
            ]

    def items(self, table_name, ids=None) -> typing.List:
        _items = list()
        table = self._get_table(table_name)
        def _get_item(id):
            item = table.get_item(
                Key=self._get_filter(
                    table_name,
                    id.model_dump(),
                ),
            )
            return None if 'Item' not in item else item['Item'] 

        if ids:
            # Ищем по ключу
            _items.extend(
                map(_get_item, ids,)
            )
        else:
            # Или забираем все записи
            scan_kwargs = {}

            while True:
                response = table.scan(**scan_kwargs)
                _items.extend(response['Items'])

                # Проверяем, есть ли ещё данные
                if 'LastEvaluatedKey' not in response:
                    break

                # Продолжаем со следующего ключа
                scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']

        return [_item for _item in _items if _item is not None]

    def delete(self, table_name, data) -> typing.List:
        table = self._get_table(table_name)
        return [
            table.delete_item(
                Key=self._get_filter(table_name, key.model_dump()),
            )
            for key in data
        ]

    def delete_all(self, table_name):
        self._client.delete_table(TableName=table_name)
        waiter = self._client.get_waiter('table_not_exists')
        waiter.wait(TableName=table_name)

        self._create_table(
            table_name,
            _MetaData().get(table_name),
        )
