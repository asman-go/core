import re
from typing import Dict, List

from asman.domains.domains.api import Domain, IncorrectDomainException


DOMAIN_PATTERN = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$'


def check_domain(domain: str) -> bool:
    if domain[:2] == '*.':
        domain = domain[2:]
    return bool(re.match(DOMAIN_PATTERN, domain))


def filter_domains(entities: Dict[str, List[str]]) -> List[Domain]:
    domains = list()
    for parent_domain in entities:
        for domain in entities[parent_domain]:
            try:
                domains.append(Domain(
                    domain=domain,
                    parent_domain=parent_domain,
                ))
            except IncorrectDomainException:
                continue

    return domains
