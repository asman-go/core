import pytest

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


@pytest.fixture
def facebook_config(monkeypatch) -> FacebookConfig:
    monkeypatch.setenv('FACEBOOK_CLIENT_ID', 'test_client_id')
    monkeypatch.setenv('FACEBOOK_CLIENT_SECRET', 'test_client_secret')
    monkeypatch.setenv('FACEBOOK_WEBHOOK_VERIFICATION_TOKEN', 'test_webhook_verification_token')
    monkeypatch.setenv('PROXY_URL', '')

    return FacebookConfig()


@pytest.fixture
def facebook_graph(facebook_config) -> FacebookGraph:
    graph = FacebookGraph(
        'https://graph.facebook.com',
        facebook_config,
    )

    return graph


@pytest.fixture
def certificate_info():
    return CertificateInfo(
        cert_hash_sha256='9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
        domains=[
            'a.example.com',
            'b.example.com',
            'example.com',
        ],
        issuer_name='DigiCert Inc',
        subject_name='*.example.com',
        id='21412512351235',
    )


@pytest.fixture
def facebook_certificate_response(certificate_info):
    return FacebookCertificateResponse(
        data=[certificate_info],
    )
