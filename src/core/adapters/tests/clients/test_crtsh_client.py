import aiohttp
import pytest
import pydantic
from pytest_mock import MockerFixture

from asman.core.adapters.clients.crtsh import CrtshClient, CertificateInfo


def test_certificate_info_create(crtsh_certificate_info_raw):
    entity = pydantic.TypeAdapter(
        CertificateInfo
    ).validate_python(
        crtsh_certificate_info_raw
    )

    assert entity
    assert entity.id == crtsh_certificate_info_raw['id']
    assert entity.common_name == crtsh_certificate_info_raw['common_name']
    assert entity.name_value == crtsh_certificate_info_raw['name_value']


def test_crtsh_client_create():
    client = CrtshClient()

    assert client
    assert client._base_url == 'https://crt.sh'


@pytest.mark.asyncio
async def test_crtsh_client_get_certificates(
            mocker: MockerFixture,
            crtsh_client: CrtshClient,
            crtsh_certificate_info: CertificateInfo
        ):
    response_mock = mocker.MagicMock(spec_set=aiohttp.ClientResponse)
    response_mock.json.return_value = [crtsh_certificate_info.model_dump()]

    async_context_mock = mocker.MagicMock(spec_set=aiohttp.ClientResponse)
    async_context_mock.__aenter__.return_value = response_mock

    mocker.patch.object(aiohttp.ClientSession, 'get', return_value=async_context_mock)

    async with crtsh_client:
        certs = await crtsh_client.get_certificates('example.com')

        assert certs
        assert len(certs) > 0
