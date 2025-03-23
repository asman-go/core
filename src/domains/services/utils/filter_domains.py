from typing import Dict, List

from asman.domains.services.api import Domain, IncorrectDomainException


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
