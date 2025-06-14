from typing import Mapping, no_type_check
import uplink
from asman.client.core import parse_response, CLIENT_UA


@uplink.headers({
    'User-Agent': CLIENT_UA,
})
class ProgramsAPI(uplink.Consumer):
    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.get('/api/private/program')
    def all(self):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.get('/api/private/program/{id}')
    def get_by_id(self, id: int):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.delete('/api/private/program/{id}')
    def remove_by_id(self, id: int):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.post('/api/private/program')
    def add(self, body: uplink.Body(Mapping)):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.json
    @uplink.put('/api/private/program/{id}')
    def update(self, id: int, body: uplink.Body(Mapping)):...
