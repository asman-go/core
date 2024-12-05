import aiohttp
import pydantic
import typing
import urllib.parse

from asman.core.adapters.clients.facebook import (
    FacebookConfig,
    FacebookCertificateResponse,
    CertificateInfo,
)


class FacebookGraph(object):
    FB_API_VERSION = "v21.0"

    _base_url: str
    _config: FacebookConfig
    _access_token: str

    def __init__(self, base_url: str, config: FacebookConfig) -> None:
        self._base_url = base_url
        self._config = config
        # https://developers.facebook.com/docs/facebook-login/guides/access-tokens#apptokens
        self._access_token = f'{self._config.FACEBOOK_CLIENT_ID}|{self._config.FACEBOOK_CLIENT_SECRET}'

        self._URL_FB_GRAPH_API_CERTIFICATES = '/certificates'
        # https://developers.facebook.com/docs/graph-api/reference/application/subscribed_domains/
        self._URL_FB_GRAPH_API_SUBSCRIBED_DOMAINS = f'/{self.FB_API_VERSION}/{self._config.FACEBOOK_CLIENT_ID}/subscribed_domains'

    async def __aenter__(self):
        await self.connect()

        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def connect(self):
        connector = aiohttp.TCPConnector(force_close=True)
        self._session = aiohttp.ClientSession(
            base_url=self._base_url,
            connector=connector,
            headers={
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate'
            }
        )

    async def _get_resource(self, url: str) -> FacebookCertificateResponse:
        
        async with self._session.get(url, proxy=self._config.PROXY_URL) as response:
            if response.ok:
                data = await response.json()
                data = pydantic.TypeAdapter(FacebookCertificateResponse).validate_python(data)

                return data
            else:
                print(response)
                return None
        
    async def get_certificates(self, domain: str) -> typing.List[CertificateInfo]:
        query = {
            'query': domain,
            'access_token': self._access_token,
            'fields': ','.join([
                'cert_hash_sha256',
                'domains',
                'issuer_name',
                'subject_name'
            ]),
            'limit': 100
        }
        resource_path = f'/certificates?{urllib.parse.urlencode(query)}'
        certificates: typing.List[CertificateInfo] = list()

        while resource_path:
            response = await self._get_resource(resource_path)
            certificates.extend(response.data)
            after = response.paging.cursors.after if response.paging and response.paging.cursors and response.paging.cursors.after else None
            query['after'] = after
            resource_path = f'/certificates?{urllib.parse.urlencode(query)}' if after else None

        return certificates

    async def subscribe(self, domains: typing.List[str]):
        body = {
            'subscribe': ','.join(domains),
            'access_token': self._access_token
        }
        async with self._session.post(self._URL_FB_GRAPH_API_SUBSCRIBED_DOMAINS, body=body, proxy=self._config.PROXY_URL) as response:
            if response.ok:
                return True
            else:
                print(response)
                return False
    
    async def unsubscribe(self, domains: typing.List[str]):
        body = {
            'unsubscribe': ','.join(domains),
            'access_token': self._access_token
        }
        async with self._session.post(self._URL_FB_GRAPH_API_SUBSCRIBED_DOMAINS, body=body, proxy=self._config.PROXY_URL) as response:
            if response.ok:
                return True
            else:
                print(response)
                return False
            
    async def get_subscribed_domains(self):
        query = {
            'fields': 'domain',
            'access_token': self._access_token
        }
        URL = f'/{self._URL_FB_GRAPH_API_SUBSCRIBED_DOMAINS}?{urllib.parse.urlencode(query)}'
        async with self._session.get(URL, proxy=self._config.PROXY_URL) as response:
            # TODO: there are pagination
            ...
            # Example:
            """
            {"data":[{"domain":"example.com","id":"1584179144975746"}],"paging":{"cursors":{"before":"QVFIU...","after":"QVFIU..."}}}
            """

        return None
