import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
import pydantic
import typing
import urllib.parse

from .models import CertificateInfo


class CrtshClient:
    _base_url: str = "https://crt.sh"

    async def __aenter__(self):
        await self.connect()

        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def connect(self):
        retry_options = ExponentialRetry(attempts=5, start_timeout=1, factor=2)
        connector = aiohttp.TCPConnector(force_close=True)
        self._session = RetryClient(
            base_url=self._base_url,
            connector=connector,
            headers={
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate'
            },
            retry_options=retry_options,
        )
        # self._session = aiohttp.ClientSession(
        #     base_url=self._base_url,
        #     connector=connector,
        #     headers={
        #         'Accept': 'application/json',
        #         'Accept-Encoding': 'gzip, deflate'
        #     }
        # )

    async def get_certificates(self, domain: str) -> typing.List[CertificateInfo]:
        query = {
            'q': domain,
            'output': 'json'
        }
        async with self._session.get(f'/?{urllib.parse.urlencode(query)}') as response:
            if response.ok:
                data = await response.json()
                data = pydantic.TypeAdapter(typing.List[CertificateInfo]).validate_python(data)

                return data
            else:
                print(response)
                return list()
