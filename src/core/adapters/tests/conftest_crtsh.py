import pytest

from asman.core.adapters.clients.crtsh import CertificateInfo, CrtshClient


@pytest.fixture
def crtsh_certificate_info_raw():
    return {
        "issuer_ca_id": 185752,
        "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert Global G2 TLS RSA SHA256 2020 CA1",
        "common_name": "www.example.org",
        "name_value": "example.com\nwww.example.com",
        "id": 12337892544,
        "entry_timestamp": "2024-03-10T20:13:50.549",
        "not_before": "2024-01-30T00:00:00",
        "not_after": "2025-03-01T23:59:59",
        "serial_number": "075bcef30689c8addf13e51af4afe187",
        "result_count": 2
    }


@pytest.fixture
def crtsh_certificate_info(crtsh_certificate_info_raw) -> CertificateInfo:
    return CertificateInfo(
        **crtsh_certificate_info_raw
    )


@pytest.fixture
def crtsh_client() -> CrtshClient:
    return CrtshClient()
