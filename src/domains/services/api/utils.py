import re

SUBDOMAIN_PATTERN = r'^[A-Za-z0-9-]{1,63}$'
TLD_PATTERN = r'^[A-Za-z]{2,}$'


def check_domain(domain: str) -> bool:
    _value = domain

    if _value.startswith('*.'):
        _value = _value[2:]
    elif _value.startswith('.'):
        _value = _value[1:]

    parts = _value.split('.')
    # check subdomain parts
    for part in parts[:-1]:
        if not bool(re.match(SUBDOMAIN_PATTERN, part)):
            return False

    # check TLD part
    if not bool(re.match(TLD_PATTERN, parts[-1])):
        return False

    return True
