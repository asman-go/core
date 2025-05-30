import pytest


# Пока не знаю как celery сюда прикрутить (в asman.core)
@pytest.mark.asyncio
async def tes1t_get_domains_from_crtsh_use_case_execute(
    domains_from_crtsh_use_case
):
    DOMAIN = 'example.com'
    domains = await domains_from_crtsh_use_case.execute([
        DOMAIN,
        # 'kinopoisk.ru',
    ])

    # print('crt.sh', domains)

    assert domains
    assert len(domains) > 0
    assert domains[0].parent_domain == DOMAIN
