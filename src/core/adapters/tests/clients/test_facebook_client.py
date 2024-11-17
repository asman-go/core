import aiohttp
import pytest
from pytest_mock import MockerFixture

from asman.core.adapters.clients.facebook import (
    FacebookConfig,
    FacebookGraph,
)
from asman.core.adapters.clients.facebook import (
    Cursor,
    Paginator,
    CertificateInfo,
    FacebookCertificateResponse,
)


def test_facebook_config_create(monkeypatch):
    FACEBOOK_CLIENT_ID = 'test_client_id'
    FACEBOOK_CLIENT_SECRET = 'test_client_secret'
    FACEBOOK_WEBHOOK_VERIFICATION_TOKEN = 'verification-token'
    monkeypatch.setenv('FACEBOOK_CLIENT_ID', FACEBOOK_CLIENT_ID)
    monkeypatch.setenv('FACEBOOK_CLIENT_SECRET', FACEBOOK_CLIENT_SECRET)
    monkeypatch.setenv('FACEBOOK_WEBHOOK_VERIFICATION_TOKEN', FACEBOOK_WEBHOOK_VERIFICATION_TOKEN)

    config = FacebookConfig()

    assert config
    assert config.FACEBOOK_CLIENT_ID == FACEBOOK_CLIENT_ID
    assert config.FACEBOOK_CLIENT_SECRET == FACEBOOK_CLIENT_SECRET
    assert config.FACEBOOK_WEBHOOK_VERIFICATION_TOKEN == FACEBOOK_WEBHOOK_VERIFICATION_TOKEN


def test_facebook_certificate_response_create():
    # TODO: Make good tests
    response = FacebookCertificateResponse(
        data=[
            CertificateInfo(
                cert_hash_sha256='test',
                domains=['test', 'test'],
                issuer_name='test',
                subject_name='test',
                id='test',
            ),
        ],
        paging=Paginator(
            cursors=Cursor(
                after='test',
                before='test',
            ),
            next='test',
        ),
    )

    assert response


def test_facebook_graph_create(facebook_config):
    graph = FacebookGraph(
        'https://graph.facebook.com',
        facebook_config,
    )

    assert graph
    assert graph._base_url == 'https://graph.facebook.com'
    assert graph._config


@pytest.mark.asyncio
async def test_facebook_graph_get_certificates(
            mocker: MockerFixture,
            facebook_graph: FacebookGraph,
            facebook_certificate_response: FacebookCertificateResponse,
        ):

    response_mock = mocker.MagicMock(spec_set=aiohttp.ClientResponse)
    response_mock.json.return_value = facebook_certificate_response.model_dump()

    async_context_mock = mocker.MagicMock(spec_set=aiohttp.ClientResponse)
    async_context_mock.__aenter__.return_value = response_mock

    # session_mock = mocker.MagicMock(spec_set=aiohttp.ClientSession)
    # session_mock.get.return_value = response_mock
    mocker.patch.object(aiohttp.ClientSession, 'get', return_value=async_context_mock)

    async with facebook_graph as fb_client:
        certs = await fb_client.get_certificates('example.com')

        assert certs
        assert len(certs) > 0


@pytest.mark.asyncio
async def test_facebook_graph_subscribe():
    # TODO: TBD
    ...


@pytest.mark.asyncio
async def test_facebook_graph_unsubscribe():
    # TBD
    ...


@pytest.mark.asyncio
async def test_facebook_graph_get_subscribed_domains():
    # TBD
    ...
