import requests
import uplink

from asman.client.clients import ProgramsAPI, ClientCRUD


class Asman(object):
    # programs: ClientCRUD[int]

    def __init__(self, api_url: str, session: requests.Session):
        self._api_url = api_url
        self._session = session
        # self._session =  requests.Session()
        # self._session.headers.update({
        #     'Authorization': 'test'
        # })

    @property
    def programs(self) -> ClientCRUD[int]:
        # self.programs = ProgramsAPI(api_url)
        return ClientCRUD(
            base_url=f'{self._api_url}/api/private/program/',
            client=uplink.RequestsClient(session=self._session),
        )
