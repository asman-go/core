from asman.core.arch import AbstractTask
from asman.core.arch import SendTaskMessage

from ._tasks import Task
from .models import (
    Domain,
    WildcardDomain
)


class WildcardDomainFormatTask(AbstractTask):
    def _call(self, message: WildcardDomain) -> Domain:
        return Domain(
            domain=message.domain.replace('*.', '')
        )
