from asman.domains.domains.api import get_domains_from_certificate


def test_get_domains_from_certificate(certificate_pem):
    parent_domain, domains = get_domains_from_certificate(certificate_pem)

    assert parent_domain == '*.example.company'
    assert domains == ['example.com', 'www.example.com', 'mail.example.com', 'ftp.example.com']
