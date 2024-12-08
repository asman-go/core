import re

DOMAIN_PATTERN = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$'


def check_domain(domain: str):
    if domain[:2] == '*.':
        domain = domain[2:]
    return bool(re.match(DOMAIN_PATTERN, domain))
