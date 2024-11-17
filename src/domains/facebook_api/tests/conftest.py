import pytest

from asman.core.adapters.tests import db_in_memory, postgres, postgres_config, facebook_config
from asman.domains.facebook_api.repo import DomainRepository
from asman.domains.facebook_api.use_cases import (
    NewCtEventUseCase,
    SubscribeNewDomainsUseCase,
)


@pytest.fixture
def certificate_pem():
    # Пример взял из своего настроенного webhook'а: https://developers.facebook.com/apps/<YOUR_FACEBOOK_CLIENT_ID>/webhooks/
    # Docs: https://developers.facebook.com/docs/graph-api/webhooks/reference/certificate_transparency/#certificate
    return "-----BEGIN CERTIFICATE-----\n        MIIFczCCA9ugAwIBAgIJAL1UADWvirO6MA0GCSqGSIb3DQEBCwUAMGUxCzAJBgNV\n        BAYTAlVTMQswCQYDVQQIEwJDQTETMBEGA1UEBxMKTWVubG8gUGFyazEYMBYGA1UE\n        ChMPRXhhbXBsZSBDb21wYW55MRowGAYDVQQDFBEqLmV4YW1wbGUuY29tcGFueTAe\n        Fw0xNjA3MjYxOTMyNTZaFw0xODA3MjYxOTMyNTZaMGUxCzAJBgNVBAYTAlVTMQsw\n        CQYDVQQIEwJDQTETMBEGA1UEBxMKTWVubG8gUGFyazEYMBYGA1UEChMPRXhhbXBs\n        ZSBDb21wYW55MRowGAYDVQQDFBEqLmV4YW1wbGUuY29tcGFueTCCAaIwDQYJKoZI\n        hvcNAQEBBQADggGPADCCAYoCggGBALfhTrbrayNZDYGf33YxLYzW7E/veNVCrYUU\n        IJYxRGS8QEPAfjbs6fPBJVaF7N/uH5M6aDt89fNHL4phvPA6q22G4QbfKj5DlTKj\n        9gzfuQLAq2UhI6JXB+yIpIRu/2rt4miCr/YkJLg1JUfDLRPVEaginbeCGNv+Rh/B\n        cDwB/TqsEnOL2PyWHGfmRLrxx6w5x2SvkzDZ2whqAAkGO2UyuW17psuuY822DmrN\n        IvR25pbZbvH7S/tPupAWd/LVIUMYtjvGLYM/fH2bzLqLjXSJDEp3mJD3D+BDx8aX\n        0yfdBIQcv8h0ypFfPT/waHmV+c6uXLh/dSdunt7e84u+XgkRyp7Ed0QydGN6lSow\n        t6JllMIufD/scO21ayV0NQOdkPZSB8xUwnjHrdJnLeSJqhd3u2CrgHXzJ8gM3x/N\n        vitoAIoDl39VKt35j9NdMZmegGRyt1ZBY1YwPJL9gTTqBkVbVMOlCwjay0d1AXBx\n        qCcWq7TlTUyjVFg5ESKEZuwrsbNr0wIDAQABo4IBJDCCASAwSgYDVR0RBEMwQYIL\n        ZXhhbXBsZS5jb22CD3d3dy5leGFtcGxlLmNvbYIQbWFpbC5leGFtcGxlLmNvbYIP\n        ZnRwLmV4YW1wbGUuY29tMAsGA1UdDwQEAwIFoDAdBgNVHQ4EFgQUpCLtkXRP2w1f\n        3LQwc0SeQUCEp7swgZcGA1UdIwSBjzCBjIAUpCLtkXRP2w1f3LQwc0SeQUCEp7uh\n        aaRnMGUxCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJDQTETMBEGA1UEBxMKTWVubG8g\n        UGFyazEYMBYGA1UEChMPRXhhbXBsZSBDb21wYW55MRowGAYDVQQDFBEqLmV4YW1w\n        bGUuY29tcGFueYIJAL1UADWvirO6MAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEL\n        BQADggGBALT1+x6IXBf9k3R6lPJ6A/B1Oo3Muj+g61kt+VDWAmEc9sUOTQDPRgI/\n        4k9/jx2GP2HCI8vC75aayU1JrcoBgOOvO6MhRckXX24SY+bbLc1kxRjWlwJf1ECh\n        QmMYfwVgHr9D4CNFYvrwY9OQo66o1bjEo6Z0RvgQnh4SSN5VE87yv9lpArP2cSdp\n        vzJZdPRj6LakPEITJrdMAeFbbwuVLf1OK6RPRFe3s46YPiYHfm51DYdZwdvrm+Vf\n        x9Aw6RCs4nQD3PqApedPm7CfN1cwMtQTYFjQyGmM0FdHXGTKIY4WIB/JmN03Md29\n        mvBdxCTrkUD7FFin1PXPgvm72E0RpAw21AfqOBeLa14w2IVkg/t4WNs8sgBT9Dij\n        Sj3Vz6/3bBSVYlhn7wxAmYK2G03mopXAUusaNc4GCF4972qYcVLdaEfLCixBNM+x\n        WntB/y2uIZuu2at5xvFFN9amIgvVdaVz5TWae43BYZElC79EUU5uiEHW58oQ82kM\n        Dw9FndMuPQ==\n        -----END CERTIFICATE-----\n        "


@pytest.fixture
def domain_repository(db_in_memory) -> DomainRepository:
    return DomainRepository(db_in_memory)


@pytest.fixture
def new_ct_event_use_case(postgres_config):
    return NewCtEventUseCase(None, postgres_config)


@pytest.fixture
def subscribe_new_domains_use_case(facebook_config, postgres_config):
    return SubscribeNewDomainsUseCase(facebook_config, postgres_config)
