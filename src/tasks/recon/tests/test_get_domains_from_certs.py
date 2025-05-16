import pytest

from asman.tasks.recon import ReconDomainsFromCertsTask


@pytest.mark.inet
@pytest.mark.asyncio
async def test_recon_domains():
    DOMAIN = 'example.com'
    payload = [DOMAIN,]
    domains = await ReconDomainsFromCertsTask(payload)

    assert domains
    assert DOMAIN in domains
    assert domains[DOMAIN]
    assert len(domains[DOMAIN]) > 0
