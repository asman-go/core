from typing import Dict, List


def join(changes1: Dict[str, List[str]], changes2: Dict[str, List[str]]):
    d = changes1.copy()
    parent_domain = changes2.keys()[0]
    if parent_domain in d:
        d[parent_domain].extend(changes2[parent_domain])
    else:
        d[parent_domain] = changes2[parent_domain]

    return d
