from asman.domains.domains.use_cases import DomainsFromCertsUseCase


def test_get_domains_from_certificates_use_case_create():
    use_case = DomainsFromCertsUseCase(None, None)

    assert use_case, 'Use case is not created'
    assert use_case.repo, 'Repo property not found'
