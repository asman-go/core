from typing import Mapping, no_type_check, TypeVar, Generic
import uplink
from asman.client.core import parse_response, CLIENT_UA


T = TypeVar('T')


@uplink.headers({
    'User-Agent': CLIENT_UA,
})
class ClientCRUD(uplink.Consumer, Generic[T]):

    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.get('')
    def all(self):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.get('{id}')
    def get_by_id(self, id: T):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.delete('{id}')
    def remove_by_id(self, id: T):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.post('')
    def add(self, body: uplink.Body(Mapping)):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.put('{id}')
    def update(self, id: T, body: uplink.Body(Mapping)):...
