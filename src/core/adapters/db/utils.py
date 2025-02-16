from enum import IntEnum
from pydantic import BaseModel
from typing import List


class Strategy(IntEnum):
    FIRST_SEEN = 0
    LAST_SEEN = 1


def unique(items: List[BaseModel], strategy: Strategy = Strategy.LAST_SEEN) -> List[BaseModel]:

    if strategy == Strategy.FIRST_SEEN:
        seen = set()
        unique_first = list()
        for item in items:
            if item not in seen:
                seen.add(item)
                unique_first.append(item)

        return unique_first

    if strategy == Strategy.LAST_SEEN:
        last_seen = dict()
        for item in items:
            last_seen[str(item)] = item

        return list(last_seen.values())

    raise Exception(f'Не реализована стратегия {strategy}')
